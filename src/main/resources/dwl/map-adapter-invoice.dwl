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
var distributorId = (p("papi.sat.solutech.distributor.id") default "1000097205") as String
var currency = (p("papi.sat.solutech.currency") default "KES") as String
---
{
	data: rows map ((sale) -> do {
		var createdAt = sale.CREATED_AT as DateTime
		---
		{
			STOREID: sale.SHOPID default "",
			Discount: sale.DISCOUNT default "",
			SalesRepID: sale.USERID default "",
			VATAmount: amount2(sale.TOTAL_VAT),
			RouteID: sale.ROUTEID default "",
			DistributorID: distributorId,
			ProductID: numericProductId(sale.PRODUCT_CODE),
			WarehouseID: sale.SUPPLIER_ID default "",
			OrderNumber: sale.SALE_ORDER_ID default "",
			InvoiceNumber: sale.ENTRY_ID default "",
			InvoiceDate: createdAt as String {format: "dd/MM/yyyy"} default "",
			InvoiceTime: createdAt as String {format: "HH:mm:ss"} default "",
			InvoiceStatus: sale.DELIVERED default "",
			UnitOfMeasure: sale.PACKAGING default "",
			Currency: currency,
			QuantityInvoiced: sale.QUANTITY default "",
			AmountInvoiced: amount2(sale.VALUE_SOLD),
			TransType: sale.ENTRY_TYPE default ""
		}
	}),
	(next: payload.next) if (payload.next != null)
}
