/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// ProductRole indicate the domain record data fields.
// ProductRole limit sell to specific roles.
type ProductRole interface {
	ProductID() ProductUUID //
	RoleID() RoleUUID       //
	Status() ProductRole_Status
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type ProductRole_StorageServices interface {
	Save(dm ProductRole) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID ProductUUID, roleID RoleUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID ProductUUID, roleID RoleUUID, vo protocol.VersionOffset) (dm ProductRole, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_ProductIDs_BY_RoleID(roleID RoleUUID, offset, limit uint64) (productIDs []ProductUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_RoleIDs_BY_ProductID(productID ProductUUID, offset, limit uint64) (roleIDs []RoleUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

type ProductRole_Status Quiddity_Status
