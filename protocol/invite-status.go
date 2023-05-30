/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// GroupInviteStatus indicate the domain record data fields.
type GroupInviteStatus interface {
	GroupID() GroupUUID             //
	UserID() UserUUID               //
	Status() GroupInvite_Status     //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type GroupInvite_Status Quiddity_Status

const (
// GroupInvite_Status_ = GroupInvite_Status(Quiddity_Status_FreeFlag << iota)
)
