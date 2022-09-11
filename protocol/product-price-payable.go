/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// ProductPricePayable indicate the domain record data fields.
// ProductPricePayable store historically price with discount to show to users in price change chart.
type ProductPricePayable interface {
	ProductID() [16]byte // product domain
	// OrgID() protocol.UserID               //
	Currency() uint64            //
	Price() protocol.MoneyAmount // Basic Price not payable price in the society currency
	Time() protocol.Time         // save time
	RequestID() UserRequestUUID  // user-request domain
}

type ProductPricePayable_StorageServices interface {
	Save(q ProductPricePayable) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID [16]byte, currency uint64) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID [16]byte, currency uint64, vo protocol.VersionOffset) (q ProductPricePayable, nv protocol.NumberOfVersion, err protocol.Error)
}
