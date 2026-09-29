%dw 2.0
output application/java
var host = trim((p("exp.sat.datashare.public.host") default p("eapi.host") default "") as String) replace /\/$/ with ""
var path = vars.inboundPath default ""
var qp = vars.inboundQueryParams default {}
var endpoint = vars.endpoint default ""
var skipDates = [
	"Adapter_Product",
	"Adapter_Route",
	"Adapter_SalesRep",
	"Adapter_Stock",
	"Adapter_Warehouse"
] contains endpoint
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
fun dropParams(q, names) =
    if ((q == null) or (q == ""))
        q
    else
        ((q splitBy "&")
            filter ((part) -> do {
                var key = (part splitBy "=")[0]
                ---
                (key != "") and not (names contains key)
            }))
        joinBy "&"
fun appendIfMissing(q, name, value) =
    if ((value == null) or ((value as String) == "") or ((q default "") contains (name ++ "=")))
        q
    else if ((q == null) or (q == ""))
        name ++ "=" ++ (value as String)
    else
        q ++ "&" ++ name ++ "=" ++ (value as String)
var downstreamQuery = queryFromNext(downstreamNext)
var cleanedQuery =
    if (downstreamQuery == null)
        null
    else
        dropParams(
            (((downstreamQuery
                replace /(&)?limit=[^&]*/ with "")
                replace /(&)?offset=[^&]*/ with "")
                replace /^&/ with ""),
            // Never expose or replay tenant selectors on the client next URL.
            if (skipDates)
                ["database", "supplier", "fromDate", "toDate"]
            else
                ["database", "supplier"]
        )
var withPage = appendIfMissing(cleanedQuery, "pageNumber", qp.pageNumber)
var clientQuery =
    if (skipDates)
        withPage
    else
        appendIfMissing(appendIfMissing(withPage, "fromDate", qp.fromDate), "toDate", qp.toDate)
---
{
    hasMore: hasMore,
    nextUrl: if ((hasMore) and (clientQuery != null) and (clientQuery != ""))
        host ++ path ++ "?" ++ clientQuery
    else
        null
}
