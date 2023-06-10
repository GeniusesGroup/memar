/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// ProductPrice indicate the domain record data fields.
// ProductPrice can be register just by producer organization whom own the related quiddity
type ProductPrice interface {
	ProductID() ProductUUID            //
	CurrencyID() FinancialCurrencyUUID //
	Price() protocol.MoneyAmount       // Basic Price, not payable price, in the currency
	Time() protocol.Time               // save time
	RequestID() urp.UserRequestUUID    //
}

type ProductPrice_StorageServices interface {
	Save(dm ProductPrice) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID ProductUUID, currencyID FinancialCurrencyUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID ProductUUID, currencyID FinancialCurrencyUUID, vo protocol.VersionOffset) (dm ProductPrice, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_ProductIDs_BY_CurrencyID_AND_Price_RANGE(currencyID FinancialCurrencyUUID, minPrice, maxPrice protocol.MoneyAmount, offset, limit uint64) (productIDs []ProductUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_CurrencyIDs_BY_ProductID(productID ProductUUID, offset, limit uint64) (currencyIDs []FinancialCurrencyUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
