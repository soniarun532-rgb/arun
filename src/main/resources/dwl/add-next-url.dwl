%dw 2.0
output application/json
var host = trim((p("eapi.host") default "") as String) replace /\/$/ with ""
var path = vars.inboundPath default ""
var qp = vars.inboundQueryParams default {}
var limitNum = (qp.limit default "10000") as Number
var offsetNum = (qp.offset default "0") as Number
var headerVal = attributes.headers['x-has-more'] default attributes.headers['X-Has-More'] default "false"
var headerHasMore = lower(headerVal as String) == "true"
var inferredHasMore = (payload is Array) and (sizeOf(payload default []) >= limitNum)
var hasMore = headerHasMore or inferredHasMore

fun toEapiUrl(url) =
    if (url == null or url == "")
        null
    else do {
        var u = url as String
        var rest =
            if (u startsWith "/")
                u
            else if (u contains "://")
                do {
                    var withoutScheme = (u splitBy "://")[1] default u
                    var slashIdx = (withoutScheme find "/")[0]
                    ---
                    if (slashIdx == null)
                        ""
                    else
                        withoutScheme[slashIdx to -1]
                }
            else
                "/" ++ u
        ---
        host ++ rest
    }

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
var builtNext = host ++ path ++ "?" ++ (builtQuery joinBy "&")
var existingNext =
    if ((payload is Object) and ((payload.next default payload.Next) != null))
        payload.next default payload.Next
    else
        null
var nextUrl =
    if (existingNext != null and existingNext != "")
        toEapiUrl(existingNext)
    else if (hasMore)
        builtNext
    else
        null
---
if (payload is Object)
    (payload - "next" - "Next") ++ { next: nextUrl }
else
    {
        data: payload,
        next: nextUrl
    }
