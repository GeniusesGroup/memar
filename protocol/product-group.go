/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// ProductGroup indicate the domain record data fields.
type ProductGroup interface {
	ProductID() [16]byte        // product domain
	GroupID() [16]byte          // group domain
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type ProductGroup_StorageServices interface {
	Save(pg ProductGroup) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID [16]byte, vo protocol.VersionOffset) (pg ProductGroup, nv protocol.NumberOfVersion, err protocol.Error)

	FindByGroup(groupID [16]byte, offset, limit uint64) (productIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}
