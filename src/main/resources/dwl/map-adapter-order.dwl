%dw 2.0
output application/json
fun numericProductId(code) = ((code default "") as String) replace /^[A-Za-z]+/ with ""
var rows = payload.data default payload default []
---
{
	data: rows map ((row) -> {
		StoreID: row.SHOP_ID default "",
		SalesRepID: row.SALES_REP default "",
		RouteID: row.ROUTEID default "",
		ProductID: numericProductId(row.PRODUCT_CODE),
		DistributorID: "???",
		WarehouseID: row.SUPPLIER_ID default "",
		OrderNumber: row.ENTRY_ID default "",
		OrderDate: if (row.CHECKINTIME == null) "" else ((row.CHECKINTIME as DateTime as String {format: "dd/MM/yyyy"}) default ""),
		OrderStartTime: if (row.CHECKINTIME == null) "" else ((row.CHECKINTIME as DateTime as String {format: "HH:mm:ss"}) default ""),
		OrderEndTime: if (row.CHECKOUTTIME == null) "" else ((row.CHECKOUTTIME as DateTime as String {format: "HH:mm:ss"}) default ""),
		OrderStatus: row.DELIVERED default "",
		UnitOfMeasure: row.PACKAGING default "",
		Currency: "KES",
		QuantityOrdered: row.QUANTITY default "",
		AmountOrdered: row.TOTAL_VAT_INC default "",
		Discount: row.DISCOUNT default "",
		VATAmount: row.TOTAL_VAT default ""
	}),
	(next: payload.next) if (payload.next != null)
}
