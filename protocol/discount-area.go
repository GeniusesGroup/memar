/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// DiscountArea indicate the domain record data fields.
// DiscountArea is proper or appropriate location indicate specific area not specific location
// It's rule depend on products in invoices e.g. source or destination of taxi as a service(product).
type DiscountArea interface {
	DiscountID() [16]byte       // discount domain
	AreaID() [16]byte           // area domain
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type DiscountArea_StorageServices interface {
	Save(da DiscountArea) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(discountID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(discountID [16]byte, vo protocol.VersionOffset) (da DiscountArea, nv protocol.NumberOfVersion, err protocol.Error)

	FindByArea(AreaID [16]byte, offset, limit uint64) (discountIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}
