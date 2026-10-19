/* For license and copyright information please see the LEGAL file in the code repository */
-- 
-- 
CREATE TABLE `Voucher` (
    `VoucherID` BINARY(16),
    `Type` SMALLINT,
    `Time` TIMESTAMP,
    `RequestID` BINARY(16),
    --
    KEY(VoucherID)
);

DELIMITER $ $ CREATE PROCEDURE Voucher_Save (
    IN `voucherID` BINARY(16),
    IN `type` SMALLINT,
    IN `time` TIMESTAMP,
    IN `requestID` BINARY(16),
    -- 
    OUT `NumberOfVersion` int
),
BEGIN -- SQL EXCEPTION
DECLARE EXIT HANDLER FOR SQLEXCEPTION,
BEGIN,
ROLLBACK;

END;

-- Everything between start transaction and commit is one atomic action. 
START TRANSACTION;

-- 
INSERT INTO
    Voucher (`VoucherID`, `Type`, `Time`, `RequestID`)
VALUES
    (`voucherID`, `type`, `time`, `requestID`);

-- 
SELECT
    COUNT(`VoucherID`) INTO `NumberOfVersion`
FROM
    Voucher
WHERE
    `VoucherID` = `voucherID`;

COMMIT;

END $ $ DELIMITER;

-- 
-- 
-- Return Count
SELECT
    COUNT(VoucherID)
FROM
    `Voucher`
WHERE
    `VoucherID` = ?;

-- 
-- Return Get 
-- TODO:: Not sure we had Time order or not!
SELECT
    *,
    COUNT(VoucherID)
FROM
    Voucher
WHERE
    `VoucherID` = ?
ORDER BY
    Voucher.Time DESC
LIMIT
    ?