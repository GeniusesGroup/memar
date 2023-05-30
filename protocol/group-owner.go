/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// GroupOwner indicate the domain record data fields.
type GroupOwner interface {
	GroupID() GroupUUID             // or ChannelID. Use to store and retrieve comments in time order. It can be UUID, URL hash or any random id.
	OwnerUserID() UserUUID          //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type GroupOwner_StorageServices interface {
	Save(g GroupOwner) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(groupID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(groupID [16]byte, vo protocol.VersionOffset) (g GroupOwner, nv protocol.NumberOfVersion, err protocol.Error)

	FindByUserID(owneruserID UserUUID, offset, limit uint64) (ids [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}
