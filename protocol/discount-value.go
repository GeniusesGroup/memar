/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// DiscountValue indicate the domain record data fields.
type DiscountValue interface {
	DiscountID() DiscountUUID       //
	Quantity() protocol.PerMyriad   // max discount percentage for each invoices, products, ... price
	Price() protocol.MoneyAmount    // max discount price can use for each invoices, product, ... price
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type DiscountValue_StorageServices interface {
	Save(dm DiscountValue) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(discountID DiscountUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(discountID DiscountUUID, vo protocol.VersionOffset) (dm DiscountValue, nv protocol.NumberOfVersion, err protocol.Error)
}
