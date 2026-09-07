%dw 2.0
import * from dwl::datashareHelpers
output application/json
var rows = payload.data default payload default []
---
{
	data: rows map ((row) -> {
		ProductID: numericProductId(v(row, ["productcode", "PRODUCTCODE"])),
		UnitofMeasure: v(row, ["UOMName", "uomname", "UOMNAME"]) default "",
		WarehouseName: v(row, ["stockpoint_name", "STOCKPOINT_NAME"]) default "",
		DateCreated: fmtDate(v(row, ["date_created", "DATE_CREATED"])),
		Quantity: v(row, ["quantity", "QUANTITY"]) default "",
		TotalCost: v(row, ["total_cost", "TOTAL_COST"]) default ""
	}),
	(next: payload.next) if (payload.next != null)
}
