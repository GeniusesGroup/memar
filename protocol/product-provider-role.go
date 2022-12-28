/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// ProductProviderRole indicate the domain record data fields.
// ProductProviderRole or product operator is to supply a particular service.
type ProductProviderRole interface {
	ProductID() [16]byte        // product domain
	RoleID() [16]byte           // role domain
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type ProductProviderRole_StorageServices interface {
	Save(pp ProductProviderRole) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID [16]byte, vo protocol.VersionOffset) (pp ProductProviderRole, nv protocol.NumberOfVersion, err protocol.Error)

	FindByRole(roleID [16]byte, offset, limit uint64) (productIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}

// related UserIDs by RoleID use to get Coordinate(domain)
