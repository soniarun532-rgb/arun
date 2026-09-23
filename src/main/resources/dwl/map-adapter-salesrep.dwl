%dw 2.0
output application/json
var rows = payload.data default payload default []
var distributorId = (p("papi.sat.solutech.distributor.id") default "1000097205") as String
---
{
	data: rows map ((row) -> {
		SalesRepID: row.id default "",
		SalesRepName: row.name default "",
		DistributorID: distributorId,
		WarehouseID: row.STOCKPOINT_ID default row.stockpoint_id default "",
		SalesRepType: row.saler_category default ""
	}),
	(next: payload.next) if (payload.next != null)
}
