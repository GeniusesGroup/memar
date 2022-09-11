/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// DiscountValue indicate the domain record data fields.
type DiscountValue interface {
	DiscountID() [16]byte         // discount domain
	Quantity() protocol.PerMyriad // max discount percentage for each invoices, products, ... price
	Price() protocol.MoneyAmount  // max discount price can use for each invoices, product, ... price
	Time() protocol.Time          // save time
	RequestID() UserRequestUUID   // user-request domain
}

type DiscountValue_StorageServices interface {
	Save(dv DiscountValue) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(discountID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(discountID [16]byte, vo protocol.VersionOffset) (dv DiscountValue, nv protocol.NumberOfVersion, err protocol.Error)
}
