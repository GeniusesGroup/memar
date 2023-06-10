/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// PosProvider indicate the domain record data fields.
// Provider or operator is to limit pos to specific staffs.
type PosProvider interface {
	PosID() PosUUID                 //
	RoleID() RoleUUID               //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type PosProvider_StorageServices interface {
	Save(dm PosProvider) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(posID PosUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(posID PosUUID, vo protocol.VersionOffset) (dm PosProvider, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_PosIDs_BY_RoleID(roleID RoleUUID, offset, limit uint64) (posIDs []PosUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

// 	LIST_RoleIDs_BY_PosID(posID PosUUID, offset, limit uint64) (roleIDs []RoleUUID, nv protocol.NumberOfVersion, err protocol.Error)
