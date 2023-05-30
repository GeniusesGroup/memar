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
	Save(dp DiscountOwner) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(discountID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(discountID [16]byte, vo protocol.VersionOffset) (dp DiscountOwner, nv protocol.NumberOfVersion, err protocol.Error)

	FindByOrg(orgID [16]byte, offset, limit uint64) (discountIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}
