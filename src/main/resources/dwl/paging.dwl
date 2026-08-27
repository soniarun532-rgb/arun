%dw 2.0
output application/java
var host = trim((p("eapi.host") default "") as String) replace /\/$/ with ""
var path = vars.inboundPath default ""
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
var hasMore = (downstreamNext != null) and (downstreamNext != "")
fun queryFromNext(url) =
    if ((url == null) or (url == ""))
        null
    else if (url contains "?")
        (url splitBy "?")[1]
    else
        null
var downstreamQuery = queryFromNext(downstreamNext)
var cleanedQuery =
    if (downstreamQuery == null)
        null
    else
        (((downstreamQuery
            replace /(&)?limit=[^&]*/ with "")
            replace /(&)?offset=[^&]*/ with "")
            replace /(&)?database=[^&]*/ with "")
            replace /(&)?supplier=[^&]*/ with "")
            replace /^&/ with ""
            replace /&&+/ with "&")
---
{
    hasMore: hasMore,
    nextUrl: if ((hasMore) and (cleanedQuery != null) and (cleanedQuery != ""))
        host ++ path ++ "?" ++ cleanedQuery
    else
        null
}
