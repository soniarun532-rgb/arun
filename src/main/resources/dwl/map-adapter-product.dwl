%dw 2.0
import * from dwl::datashareHelpers
output application/json
var rows = payload.data default payload default []
---
{
	data: rows map ((row) -> {
		id: v(row, ["id", "ID"]) default "",
		ProductID: numericProductId(v(row, ["productcode", "PRODUCTCODE"])),
		product_category: v(row, ["product_category", "PRODUCT_CATEGORY"]) default "",
		product_name: v(row, ["product_name", "PRODUCT_NAME"]) default "",
		ProductSKU: v(row, ["product_desc", "PRODUCT_DESC"]) default "",
		product_status: v(row, ["product_status", "PRODUCT_STATUS"]) default "",
		short_code: v(row, ["short_code", "SHORT_CODE"]) default "",
		tax_code: v(row, ["tax_code", "TAX_CODE"]) default "",
		hs_code: v(row, ["hs_code", "HS_CODE"]) default "",
		focus_product: v(row, ["focus_product", "FOCUS_PRODUCT"]) default "",
		tonne_equivalent: v(row, ["tonne_equivalent", "TONNE_EQUIVALENT"]) default "",
		apply_discount: v(row, ["apply_discount", "APPLY_DISCOUNT"]) default "",
		disable_price_check: v(row, ["disable_price_check", "DISABLE_PRICE_CHECK"]) default "",
		product_type: v(row, ["product_type", "PRODUCT_TYPE"]) default "",
		supplier: v(row, ["supplier", "SUPPLIER"]) default "",
		alternative_group: v(row, ["alternative_group", "ALTERNATIVE_GROUP"]) default "",
		supplier_id: v(row, ["supplier_id", "SUPPLIER_ID"]) default "",
		UnitofMeasure: v(row, ["uomname", "UOMName", "UOMNAME"]) default ""
	}),
	(next: payload.next) if (payload.next != null)
}
