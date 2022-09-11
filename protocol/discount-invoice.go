/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// DiscountInvoice indicate the domain record data fields.
type DiscountInvoice interface {
	DiscountID() [16]byte           // discount domain
	MinPrice() protocol.MoneyAmount // Minimum invoice price
	MinAmount() uint64              // Minimum invoice product numbers
	Time() protocol.Time            // save time
	RequestID() UserRequestUUID     // user-request domain
}

type DiscountInvoice_StorageServices interface {
	Save(di DiscountInvoice) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(discountID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(discountID [16]byte, vo protocol.VersionOffset) (di DiscountInvoice, nv protocol.NumberOfVersion, err protocol.Error)
}
