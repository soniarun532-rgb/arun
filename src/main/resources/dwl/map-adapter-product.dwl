%dw 2.0
output application/json
fun productIdFromCode(code) = ((code default "") as String) replace /^[A-Za-z]+/ with ""
var rows = payload.data default payload default []
---
{
	data: rows map ((row) -> {
		id: row.id default "",
		ProductID: productIdFromCode(row.productcode),
		product_category: row.product_category default "",
		product_name: row.product_name default "",
		ProductSKU: row.product_desc default "",
		product_status: row.product_status default "",
		short_code: row.short_code default "",
		tax_code: row.tax_code default "",
		hs_code: row.hs_code default "",
		focus_product: row.focus_product default "",
		tonne_equivalent: row.tonne_equivalent default "",
		apply_discount: row.apply_discount default "",
		disable_price_check: row.disable_price_check default "",
		product_type: row.product_type default "",
		supplier: row.supplier default "",
		alternative_group: row.alternative_group default "",
		supplier_id: row.supplier_id default "",
		UnitofMeasure: row.uomname default ""
	}),
	(next: payload.next) if (payload.next != null)
}
