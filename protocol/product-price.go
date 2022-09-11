/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// ProductPrice indicate the domain record data fields.
// ProductPrice can be register just by producer organization whom own the related quiddity
type ProductPrice interface {
	ProductID() [16]byte         // product domain
	Currency() [16]byte          // financial-currency
	Price() protocol.MoneyAmount // Basic Price not payable price in the currency
	Time() protocol.Time         // save time
	RequestID() UserRequestUUID  // user-request domain
}

type ProductPrice_StorageServices interface {
	Save(pp ProductPrice) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID [16]byte, currency uint64) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID [16]byte, currency uint64, vo protocol.VersionOffset) (pp ProductPrice, nv protocol.NumberOfVersion, err protocol.Error)

	ListProductCurrencies(productID [16]byte, offset, limit uint64) (currencies []uint64, nv protocol.NumberOfVersion, err protocol.Error)
}
