/* For license and copyright information please see the LEGAL file in the code repository */
-- 
CREATE TABLE InvoiceVoucher (
    InvoiceID BINARY(16) NOT NULL,
    VoucherID BINARY(16) NOT NULL,
    Discounted DECIMAL(9, 2) NOT NULL,
    Time TIMESTAMP NOT NULL,
    RequestID BINARY(16) NOT NULL,
    -- PRIMARY KEY (InvoiceID)
),
INDEX index_InvoiceVoucher_on_InvoiceID (InvoiceID),
INDEX index_InvoiceVoucher_on_VoucherID (VoucherID);
-- 
-- name: Save :exec
INSERT INTO InvoiceVoucher
VALUES (?, ?, ?, ?, ?);
RETURNING COUNT(InvoiceID);
-- 
-- name: Count :one
SELECT COUNT(InvoiceID)
FROM table_name
WHERE InvoiceID = ?;
-- 
-- name: Get :many
SELECT *
FROM InvoiceVoucher
ORDER BY name;
-- 
SELECT *
FROM InvoiceVoucher
WHERE id = ?
LIMIT 1;
-- 
-- name: FindByVoucherID :execresult
INSERT INTO InvoiceVoucher (name, bio)
VALUES (?, ?);