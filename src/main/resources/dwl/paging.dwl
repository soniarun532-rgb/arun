%dw 2.0
output application/java
var host = trim((p("eapi.host") default "") as String) replace /\/$/ with ""
var path = vars.inboundPath default ""
var qp = vars.inboundQueryParams default {}
var limitNum = (qp.limit default "10000") as Number
var offsetNum = (qp.offset default "0") as Number
var headerHasMore = lower((vars.lastCallHasMore default "false") as String) == "true"
var inferredHasMore = (payload is Array) and (sizeOf(payload default []) >= limitNum)
var hasMore = headerHasMore or inferredHasMore

fun qsPair(name, value) =
    if (value == null or value == "")
        null
    else
        name ++ "=" ++ (value as String)

var builtQuery = [
    qsPair("fromDate", qp.fromDate),
    qsPair("toDate", qp.toDate),
    qsPair("limit", limitNum as String),
    qsPair("offset", (offsetNum + limitNum) as String)
] filter ((item) -> item != null)
---
{
    hasMore: hasMore,
    nextUrl: if (hasMore) (host ++ path ++ "?" ++ (builtQuery joinBy "&")) else null
}
