%dw 2.0
output application/json
fun numericProductId(code) = ((code default "") as String) replace /^[A-Za-z]+/ with ""
var rows = payload.data default payload default []
---
{
	data: rows map ((sale) -> do {
		var createdAt = sale.CREATED_AT as DateTime
		---
		{
			STOREID: sale.SHOPID default "",
			Discount: sale.DISCOUNT default "",
			SalesRepID: sale.USERID default "",
			VATAmount: sale.TOTAL_VAT default "",
			RouteID: sale.ROUTEID default "",
			DistributorID: "",
			ProductID: numericProductId(sale.PRODUCT_CODE),
			WarehouseID: sale.SUPPLIER_ID default "",
			OrderNumber: sale.SALE_ORDER_ID default "",
			InvoiceNumber: sale.ENTRY_ID default "",
			InvoiceDate: createdAt as String {format: "dd/MM/yyyy"} default "",
			InvoiceTime: createdAt as String {format: "HH:mm:ss"} default "",
			InvoiceStatus: sale.PAYMENT_STATUS default "",
			UnitOfMeasure: sale.PACKAGING default "",
			Currency: "KES",
			QuantityInvoiced: sale.QUANTITY default "",
			AmountInvoiced: sale.VALUE_SOLD default "",
			TransType: sale.ENTRY_TYPE default ""
		}
	}),
	(next: payload.next) if (payload.next != null)
}
