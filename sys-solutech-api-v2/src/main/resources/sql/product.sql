-- Endpoint D: GET /api/Product
-- D = bi_products
-- Filter: supplier = :Supplier
-- Paging: LIMIT pageSize OFFSET (PageNumber-1)*pageSize

SELECT
	id AS ProductID,
	productcode AS ProductCode,
	product_category AS ProductCategory,
	product_name AS ProductName,
	product_desc AS ProductDescription,
	product_status AS ProductStatus,
	short_code AS ShortCode,
	tax_code AS TaxCode,
	hs_code AS HsCode,
	product_type AS ProductType,
	supplier AS Supplier
FROM {Database}.bi_products
WHERE supplier = :Supplier
ORDER BY id
LIMIT :limit OFFSET :offset
