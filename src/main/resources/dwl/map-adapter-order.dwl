%dw 2.0
import * from dwl::datashareHelpers
output application/json
var rows = payload.data default payload default []
---
{
	data: rows map ((row) -> {
		StoreID: s(row, ["SHOP_ID", "SHOPID"]),
		SalesRepID: s(row, ["SALES_REP", "SALESREP"]),
		RouteID: s(row, ["routeid", "ROUTEID"]),
		ProductID: numericProductId(v(row, ["PRODUCT_code", "PRODUCT_CODE", "PRODUCTCODE"])),
		DistributorID: (p("papi.sat.solutech.distributor.id") default "") as String,
		WarehouseID: s(row, ["supplier_id", "SUPPLIER_ID"]),
		OrderNumber: s(row, ["ENTRY_ID"]),
		OrderDate: fmtDate(v(row, ["CHECKINTIME", "CHECK_IN_TIME"])),
		OrderStartTime: fmtTime(v(row, ["CHECKINTIME"])),
		OrderEndTime: fmtTime(v(row, ["CHECKOUTTIME"])),
		OrderStatus: v(row, ["DELIVERED"]) default "",
		UnitOfMeasure: s(row, ["PACKAGING"]),
		Currency: (p("papi.sat.solutech.currency") default "KES") as String,
		QuantityOrdered: v(row, ["QUANTITY"]) default "",
		AmountOrdered: v(row, ["TOTAL_VAT_INC"]) default "",
		Discount: v(row, ["DISCOUNT"]) default "",
		VATAmount: v(row, ["TOTAL_VAT"]) default ""
	}),
	(next: payload.next) if (payload.next != null)
}
