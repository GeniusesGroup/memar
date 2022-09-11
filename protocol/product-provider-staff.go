/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// ProductProvider indicate the domain record data fields.
type ProductProviderStaff interface {
	ProductID() [16]byte        // product domain
	StaffID() [16]byte          // staff domain
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type ProductProviderStaff_StorageServices interface {
	Save(pp ProductProviderStaff) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID [16]byte, vo protocol.VersionOffset) (pp ProductProviderStaff, nv protocol.NumberOfVersion, err protocol.Error)

	FindByStaff(staffID [16]byte, offset, limit uint64) (productIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}

// related UserIDs by StaffID use to get Coordinate(domain)
