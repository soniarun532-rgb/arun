-- Endpoint C: GET /api/Sales
-- A = bi_salesmaster, B = bi_customer_visits
-- Filters: A.Created_AT between fromDate 00:00:00 and toDate 00:00:00
-- Optional: A.product_id IN (Product_ID list)
-- Paging: LIMIT pageSize OFFSET (PageNumber-1)*pageSize

SELECT
	a.SHOPID AS STOREID,
	a.USERID AS SalesRepID,
	b.routeid AS RouteID,
	a.product_id AS ProductID,
	'???' AS DistributorID,
	a.Supplier_id AS WarehouseID,
	a.SALE_ORDER_ID AS OrderNumber,
	a.Entry_ID AS InvoiceNumber,
	DATE_FORMAT(a.Created_AT, '%d/%m/%Y') AS InvoiceDate,
	DATE_FORMAT(a.Created_AT, '%H:%i:%s') AS InvoiceTimepart,
	a.Payment_Status AS InvoiceStatus,
	a.packaging AS UnitOfMeasure,
	'KES' AS Currency,
	a.quantity AS QuantityInvoiced,
	a.value_sold AS AmountInvoiced,
	'???' AS Discount,
	'???' AS VATAmount,
	a.Entry_Type AS TransType
FROM {Database}.bi_salesmaster AS a
LEFT JOIN {Database}.bi_customer_visits AS b
	ON a.VisitID = b.visitid
WHERE a.Created_AT BETWEEN :fromTs AND :toTs
	-- AND a.product_id IN (:Product_ID)  /* when Product_ID is sent */
ORDER BY a.Created_AT, a.Entry_ID
LIMIT :limit OFFSET :offset
