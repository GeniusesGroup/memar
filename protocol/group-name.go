/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// GroupName indicate the domain record data fields.
// It is not the group title as display name, It is the unique group name.
type GroupName interface {
	GroupID() GroupUUID             //
	Name() string                   // It is not replace of group ID. It usually use to find the group in more human friendly manner.
	Status() GroupName_Status       //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type GroupName_StorageServices interface {
	Save(gn GroupName) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(groupID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(groupID [16]byte, vo protocol.VersionOffset) (gn GroupName, nv protocol.NumberOfVersion, err protocol.Error)

	FindByName(name string, offset, limit uint64) (groupIDs [][16]byte, err protocol.Error)
}

// GroupName_Status indicate GroupName record status
type GroupName_Status uint8

// GroupName status
const (
	GroupName_Status_Unset    GroupName_Status = 0
	GroupName_Status_Register GroupName_Status = (1 << iota)
	GroupName_Status_Remove
	GroupName_Status_Blocked
	GroupName_Status_Reserved
)
