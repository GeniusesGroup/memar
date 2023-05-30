/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// ProductPrice indicate the domain record data fields.
// ProductPrice can be register just by producer organization whom own the related quiddity
type ProductPrice interface {
	ProductID() ProductUUID          //
	Currency() FinancialCurrencyUUID //
	Price() protocol.MoneyAmount     // Basic Price not payable price in the currency
	Time() protocol.Time             // save time
	RequestID() urp.UserRequestUUID  //
}

type ProductPrice_StorageServices interface {
	Save(pp ProductPrice) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID ProductUUID, currency uint64) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID ProductUUID, currency uint64, vo protocol.VersionOffset) (pp ProductPrice, nv protocol.NumberOfVersion, err protocol.Error)

	ListProductCurrencies(productID ProductUUID, offset, limit uint64) (currencies []FinancialCurrencyUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
