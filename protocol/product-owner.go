/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// ProductOwner indicate the domain record data fields.
type ProductOwner interface {
	ProductID() [16]byte        // product domain
	OrgID() protocol.UserID     // user domain
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type ProductOwner_StorageServices interface {
	Save(po ProductOwner) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID [16]byte, vo protocol.VersionOffset) (po ProductOwner, nv protocol.NumberOfVersion, err protocol.Error)

	FindByOrg(orgID [16]byte, offset, limit uint64) (productIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}
