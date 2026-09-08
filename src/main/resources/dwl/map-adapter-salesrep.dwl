%dw 2.0
output application/json
var rows = payload.data default payload default []
---
{
	data: rows map ((row) -> {
		SalesRepID: row.id default "",
		SalesRepName: row.name default "",
		DistributorID: "???",
		WarehouseID: row.warehouse_code default "",
		SalesRepType: row.saler_category default ""
	}),
	(next: payload.next) if (payload.next != null)
}
