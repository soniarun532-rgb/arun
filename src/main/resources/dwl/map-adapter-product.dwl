%dw 2.0
output application/json
fun productIdFromCode(code) = ((code default "") as String) replace /^[A-Za-z]+/ with ""
var rows = payload.data default payload default []
---
{
	data: rows map ((row) -> {
		ProductID: productIdFromCode(row.productcode),
		ProductSKU: row.product_desc default "",
		UnitofMeasure: row.uomname default row.UOMName default ""
	}),
	(next: payload.next) if (payload.next != null)
}
