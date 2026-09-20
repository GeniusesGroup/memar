/* For license and copyright information please see the LEGAL file in the code repository */
-- 
CREATE TABLE InvoiceVoucher (
    InvoiceID BINARY(16) NOT NULL,
    VoucherID BINARY(16) NOT NULL,
    Discounted protocol.AmountOfMoney NOT NULL,
    Time protocol.Time NOT NULL,
    RequestID BINARY(16) NOT NULL,
    KEY (InvoiceID) -- PRIMARY but not UNIQUE
    KEY (VoucherID)
);
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
-- name: Get :one
SELECT *
FROM InvoiceVoucher
WHERE InvoiceID = ?
LIMIT 1 OFFSET ?;