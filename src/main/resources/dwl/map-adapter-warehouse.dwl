%dw 2.0
output application/json
var rows = payload.data default payload default []
---
{
	data: rows map ((row) -> {
		WarehouseID: row.ID default "",
		WarehouseName: row.CUSTOMERNAME default "",
		DistributorID: ""
	}),
	(next: payload.next) if (payload.next != null)
}
