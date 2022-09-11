/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// GroupAssociatedStatus indicate the domain record data fields
type GroupAssociatedStatus interface {
	GroupID() [16]byte              // group domain
	UserID() protocol.UserID        // user domain
	Status() GroupAssociated_Status //
	Time() protocol.Time            // save time
	RequestID() UserRequestUUID     // user-request domain
}

type GroupAssociated_Status Quiddity_Status

const (
	GroupAssociated_Status_Joined = GroupAssociated_Status(Quiddity_Status_FreeFlag << iota)
	GroupAssociated_Status_Blocked
	GroupAssociated_Status_Muted
)
