/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// ProductPricePayable indicate the domain record data fields.
// ProductPricePayable store historically price with discount to show to users in price change chart.
type ProductPricePayable interface {
	ProductID() ProductUUID //
	// OrgID() OrgUUID              //
	Currency() uint64               //
	Price() protocol.MoneyAmount    // Basic Price not payable price in the society currency
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type ProductPricePayable_StorageServices interface {
	Save(q ProductPricePayable) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID ProductUUID, currency uint64) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID ProductUUID, currency uint64, vo protocol.VersionOffset) (q ProductPricePayable, nv protocol.NumberOfVersion, err protocol.Error)
}
