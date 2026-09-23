%dw 2.0
output application/json
var rows = payload.data default payload default []
var distributorId = (p("papi.sat.solutech.distributor.id") default "1000097205") as String
---
{
	data: rows map ((row) -> {
		WarehouseID: row.ID default "",
		WarehouseName: row.CUSTOMERNAME default "",
		DistributorID: distributorId
	}),
	(next: payload.next) if (payload.next != null)
}
