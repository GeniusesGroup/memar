/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// DiscountArea indicate the domain record data fields.
// DiscountArea is proper or appropriate location indicate specific area not specific location
// It's rule depend on products in invoices e.g. source or destination of taxi as a service(product).
type DiscountArea interface {
	DiscountID() DiscountUUID       //
	EstateID() EstateUUID           
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type DiscountArea_StorageServices interface {
	Save(dm DiscountArea) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(discountID DiscountUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(discountID DiscountUUID, vo protocol.VersionOffset) (dm DiscountArea, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_DiscountIDs_BY_EstateID(EstateID EstateUUID, offset, limit uint64) (discountIDs []DiscountUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
