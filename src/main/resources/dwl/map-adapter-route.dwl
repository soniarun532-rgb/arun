%dw 2.0
output application/json
var rows = payload.data default payload default []
---
{
	data: rows map ((row) -> {
		RouteID: row.route_id default "",
		RouteName: row.route_name default "",
		SalesRepID: row.userid default "",
		RouteType: row.visit_frequency default "",
		SalesRepType: row.saler_category default "",
		Date: if (row.created_at == null) "" else ((row.created_at as DateTime as String {format: "dd/MM/yyyy"}) default "")
	}),
	(next: payload.next) if (payload.next != null)
}
