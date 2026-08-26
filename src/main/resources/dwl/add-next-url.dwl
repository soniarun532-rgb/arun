%dw 2.0
output application/json
var records =
    if ((payload is Object) and (payload.data is Object) and (payload.data.data != null))
        payload.data.data
    else if ((payload is Object) and (payload.data != null))
        payload.data
    else
        payload
---
{
    data: records,
    next: vars.paging.nextUrl default null
}
