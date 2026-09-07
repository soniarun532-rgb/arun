%dw 2.0
output application/json
var rows = payload.data default payload default []
---
{
	data: rows,
	(next: payload.next) if (payload.next != null)
}
