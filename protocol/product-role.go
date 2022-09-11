/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// ProductRole indicate the domain record data fields.
// ProductRole limit sell to specific roles.
type ProductRole interface {
	ProductID() [16]byte        // product domain
	RoleID() [16]byte           // role domain
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type ProductRole_StorageServices interface {
	Save(pr ProductRole) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID [16]byte, vo protocol.VersionOffset) (pr ProductRole, nv protocol.NumberOfVersion, err protocol.Error)

	FindByRole(roleID [16]byte, offset, limit uint64) (productIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}
