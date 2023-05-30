/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// ProductRole indicate the domain record data fields.
// ProductRole limit sell to specific roles.
type ProductRole interface {
	ProductID() ProductUUID         //
	RoleID() RoleUUID               //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type ProductRole_StorageServices interface {
	Save(pr ProductRole) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID ProductUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID ProductUUID, vo protocol.VersionOffset) (pr ProductRole, nv protocol.NumberOfVersion, err protocol.Error)

	FindByRole(roleID RoleUUID, offset, limit uint64) (productIDs []ProductUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
