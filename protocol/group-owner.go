/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// GroupOwner indicate the domain record data fields.
type GroupOwner interface {
	GroupID() GroupUUID             // or ChannelID. Use to store and retrieve comments in time order. It can be UUID, URL hash or any random id.
	OwnerUserID() up.UserUUID       //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type GroupOwner_StorageServices interface {
	Save(dm GroupOwner) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(groupID GroupUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(groupID GroupUUID, vo protocol.VersionOffset) (dm GroupOwner, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_GroupIDs_BY_OwnerUserID(ownerUserID up.UserUUID, offset, limit uint64) (groupIDs []GroupUUID, nv protocol.NumberOfVersion, err protocol.Error)

	// only one owner or it could be a list of owners ??
}
