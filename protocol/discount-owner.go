/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// DiscountOwner indicate the domain record data fields.
type DiscountOwner interface {
	DiscountID() DiscountUUID       //
	OrgID() OrgUUID                 //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type DiscountOwner_StorageServices interface {
	Save(dm DiscountOwner) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(discountID DiscountUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(discountID DiscountUUID, vo protocol.VersionOffset) (dm DiscountOwner, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_DiscountIDs_BY_OrgID(orgID OrgUUID, offset, limit uint64) (discountIDs []DiscountUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
