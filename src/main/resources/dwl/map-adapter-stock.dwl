%dw 2.0
output application/json
fun fromFirstNumeric(code) = ((code default "") as String) replace /^[A-Za-z]+/ with ""
var rows = payload.data default payload default []
---
{
	data: rows map ((row) -> {
		ProductSKU: fromFirstNumeric(row.productcode),
		UnitofMeasure: row.uomname default "",
		DistributorWarehouseCode: row.stockpoint_name default "",
		Date: if (row.date_created == null) "" else ((row.date_created as DateTime as String {format: "dd/MM/yyyy"}) default ""),
		InventoryQuantity: row.quantity default "",
		InventoryPrice: row.total_cost default ""
	}),
	(next: payload.next) if (payload.next != null)
}
