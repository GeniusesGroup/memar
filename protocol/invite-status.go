/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// GroupInviteStatus indicate the domain record data fields.
type GroupInviteStatus interface {
	GroupID() [16]byte          // group domain
	UserID() protocol.UserID    // user domain
	Status() GroupInvite_Status //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type GroupInvite_Status = Quiddity_Status

const (
// GroupInvite_Status_ = GroupInvite_Status(Quiddity_Status_FreeFlag << iota)
)
