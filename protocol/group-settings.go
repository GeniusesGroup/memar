/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// GroupRole indicate the domain record data fields.
type GroupSettings interface {
	GroupID() [16]byte                     // group domain
	ArchiveThreadAfter() protocol.Duration //
	BlockedWords() []string                //
	Join() GroupSettings                   //
	Time() protocol.Time                   // save time
	RequestID() UserRequestUUID            // user-request domain
}

type GroupSettings_StorageServices interface {
	Save(gs GroupSettings) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(groupID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(groupID [16]byte, vo protocol.VersionOffset) (gs GroupSettings, nv protocol.NumberOfVersion, err protocol.Error)
}

type GroupSettings_Join uint8

const (
	GroupSettings_Join_Unset  GroupSettings_Join = 0
	GroupSettings_Join_Invite GroupSettings_Join = (1 << iota)
	GroupSettings_Join_AddByMembers
)
