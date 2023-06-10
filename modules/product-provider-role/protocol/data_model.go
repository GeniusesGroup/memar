/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// ProductProviderRole indicate the domain record data fields.
// ProductProviderRole or product operator is to supply a particular service.
// TODO::: role or group??
type ProductProviderRole interface {
	ProductID() ProductUUID //
	RoleID() RoleUUID       //
	Status() ProductProviderRole_Status
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type ProductProviderRole_StorageServices interface {
	Save(dm ProductProviderRole) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID ProductUUID, roleID RoleUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID ProductUUID, roleID RoleUUID, vo protocol.VersionOffset) (dm ProductProviderRole, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_ProductIDs_BY_RoleID(roleID RoleUUID, offset, limit uint64) (productIDs []ProductUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_RoleIDs_BY_ProductID(productID ProductUUID, offset, limit uint64) (roleIDs []RoleUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

type ProductProviderRole_Status Quiddity_Status

// related UserIDs by RoleID use to get Coordinate(domain)
