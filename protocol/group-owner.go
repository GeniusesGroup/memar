/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// GroupOwner indicate the domain record data fields.
type GroupOwner interface {
	GroupID() [16]byte            // or ChannelID. Use to store and retrieve comments in time order. It can be UUID, URL hash or any random id.
	OwnerUserID() protocol.UserID // user domain
	Time() protocol.Time          // save time
	RequestID() UserRequestUUID   // user-request domain
}

type GroupOwner_StorageServices interface {
	Save(g GroupOwner) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(groupID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(groupID [16]byte, vo protocol.VersionOffset) (g GroupOwner, nv protocol.NumberOfVersion, err protocol.Error)

	FindByUserID(ownerUserID [16]byte, offset, limit uint64) (ids [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}
