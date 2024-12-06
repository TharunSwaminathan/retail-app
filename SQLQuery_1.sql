-- -- CREATE TABLE Households5 (
-- --     HSHD_NUM INT PRIMARY KEY, -- Household number
-- --     L CHAR(1) NULL, -- Single-character column
-- --     AGE_RANGE VARCHAR(100) NULL, -- Increased length for age range
-- --     MARITAL VARCHAR(50) NULL, -- Increased length for marital status
-- --     INCOME_RANGE VARCHAR(100) NULL, -- Increased length for income range
-- --     HOMEOWNER VARCHAR(20) NULL, -- Increased length for homeowner status
-- --     HSHD_COMPOSITION VARCHAR(100) NULL, -- Increased length for household composition
-- --     HH_SIZE VARCHAR(50) NULL, -- Increased length for household size
-- --     CHILDREN VARCHAR(50) NULL -- Increased length for number of children
-- -- );

-- ALTER TABLE Households5 ALTER COLUMN HH_SIZE VARCHAR(50) NULL;

-- CREATE TABLE Products (
--     PRODUCT_NUM INT PRIMARY KEY, -- Unique product number
--     DEPARTMENT VARCHAR(100), -- DEPARTMENT the product belongs to
--     COMMODITY VARCHAR(100), -- Product commodity or category
--     BRAND_TY VARCHAR(50), -- Brand type (e.g., national, private)
--     NATURAL_ORGANIC_FLAG CHAR(1) -- Indicator for natural or organic product ('Y' or 'N')
-- );




-- CREATE TABLE Transactions3 (
--     BASKET_NUM INT, -- Unique identifier for each basket
--     HSHD_NUM INT, -- Household number (foreign key to Households table)
--     PURCHASE_ VARCHAR(50), -- PURCHASE_ of the purchase
--     PRODUCT_NUM INT, -- Product number (foreign key to Products table)
--     SPEND DECIMAL(10, 2), -- Amount spent on the transaction
--     UNITS INT, -- Number of units purchased
--     STORE_R VARCHAR(50), -- Store region
--     WEEK_NUM INT, -- Week of the year
--     YEAR INT -- Year of the transaction
-- );


-- Delete FROM dbo.Households5

-- Delete FROM dbo.Products

-- Delete FROM dbo.Transactions3

-- SELECT 
--     h.HSHD_NUM,
--     t.BASKET_NUM,
--     t.PURCHASE_,
--     t.PRODUCT_NUM,
--     p.DEPARTMENT,
--     p.COMMODITY,
--     t.SPEND,
--     t.UNITS,
--     t.STORE_R,
--     t.WEEK_NUM,
--     t.YEAR,
--     h.L,
--     h.AGE_RANGE,
--     h.MARITAL,
--     h.INCOME_RANGE,
--     h.HOMEOWNER,
--     h.HSHD_COMPOSITION,
--     h.HH_SIZE,
--     h.CHILDREN
-- FROM 
--     dbo.Households5 h
-- JOIN 
--     dbo.Transactions3 t
--     ON h.HSHD_NUM = t.HSHD_NUM
-- JOIN 
--     dbo.Products p
--     ON t.PRODUCT_NUM = p.PRODUCT_NUM
-- WHERE 
--     h.HSHD_NUM = 10;
