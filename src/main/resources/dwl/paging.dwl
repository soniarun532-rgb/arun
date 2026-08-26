%dw 2.0
output application/java
var host = trim((p("eapi.host") default "") as String) replace /\/$/ with ""
var path = vars.inboundPath default ""
var qp = vars.inboundQueryParams default {}
var limitNum = (qp.limit default "10000") as Number
var records =
    if ((payload is Object) and (payload.data is Object) and (payload.data.data != null))
        payload.data.data
    else if ((payload is Object) and (payload.data != null))
        payload.data
    else
        payload
var downstreamNext =
    if (payload is Object)
        payload.next default payload.data.next default null
    else
        null
var headerHasMore = lower((vars.lastCallHasMore default "false") as String) == "true"
var inferredHasMore = (records is Array) and (sizeOf(records default []) >= limitNum)
var hasMore = headerHasMore or inferredHasMore or ((downstreamNext != null) and (downstreamNext != ""))

fun queryFromNext(url) =
    if ((url == null) or (url == ""))
        null
    else if (url contains "?")
        (url splitBy "?")[1]
    else
        null

fun qsPair(name, value) =
    if (value == null or value == "")
        null
    else
        name ++ "=" ++ (value as String)

var downstreamQuery = queryFromNext(downstreamNext)
var builtQuery = [
    qsPair("fromDate", qp.fromDate),
    qsPair("toDate", qp.toDate),
    qsPair("limit", qp.limit default "10000"),
    qsPair("offset", ((qp.offset default "0") as Number + limitNum) as String)
] filter ((item) -> item != null)
var nextUrl =
    if (downstreamQuery != null)
        host ++ path ++ "?" ++ downstreamQuery
    else if (hasMore)
        host ++ path ++ "?" ++ (builtQuery joinBy "&")
    else
        null
---
{
    hasMore: hasMore,
    nextUrl: nextUrl
}
