/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// DiscountInvoice indicate the domain record data fields.
type DiscountInvoice interface {
	DiscountID() DiscountUUID       //
	MinPrice() protocol.MoneyAmount // Minimum invoice price
	MinAmount() uint64              // Minimum invoice product numbers
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type DiscountInvoice_StorageServices interface {
	Save(dm DiscountInvoice) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(discountID DiscountUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(discountID DiscountUUID, vo protocol.VersionOffset) (dm DiscountInvoice, nv protocol.NumberOfVersion, err protocol.Error)
}
