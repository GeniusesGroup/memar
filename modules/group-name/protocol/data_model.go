/* For license and copyright information please see the LEGAL file in the code repository */

package gnp

import (
	"libgo/protocol"

	gp "org/modules/group/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
// It is not the group title as display name, It is the unique group name.
type DataModel interface {
	GroupID() gp.GroupUUID          //
	Name() string                   // It is not replace of group ID. It usually use to find the group in more human friendly manner.
	Status() Status                 //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

// Status indicate GroupName record status
type Status uint8

// GroupName status
const (
	Status_Unset    Status = 0
	Status_Register Status = (1 << iota)
	Status_Remove
	Status_Blocked
	Status_Reserved
)
