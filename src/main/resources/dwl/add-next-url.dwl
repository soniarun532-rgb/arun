%dw 2.0
output application/json
---
{
    data: payload,
    next: vars.paging.nextUrl default null
}
