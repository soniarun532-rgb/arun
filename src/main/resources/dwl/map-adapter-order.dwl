%dw 2.0
output application/json
fun numericProductId(code) = ((code default "") as String) replace /^[A-Za-z]+/ with ""
fun amount2(value) =
	if ((value == null) or (value == ""))
		""
	else do {
		var n = value as Number default null
		---
		if (n == null) ((value as String) default "")
		else n as String {format: "0.00"}
	}
var rows = payload.data default payload default []
var currency = (p("papi.sat.solutech.currency") default "KES") as String
---
{
	data: rows map ((row) -> {
		StoreID: row.SHOP_ID default "",
		SalesRepID: row.USER_ID default row.user_id default row.USERID default "",
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
		Currency: currency,
		QuantityOrdered: row.QUANTITY default "",
		AmountOrdered: row.TOTAL_VAT_INC default "",
		Discount: row.DISCOUNT default "",
		VATAmount: amount2(row.TOTAL_VAT)
	}),
	(next: payload.next) if (payload.next != null)
}
