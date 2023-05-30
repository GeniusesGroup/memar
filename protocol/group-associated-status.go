/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// GroupAssociatedStatus indicate the domain record data fields
type GroupAssociatedStatus interface {
	GroupID() GroupUUID             //
	UserID() up.UserUUID            //
	Status() GroupAssociated_Status //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type GroupAssociated_Status Quiddity_Status

const (
	GroupAssociated_Status_Joined = GroupAssociated_Status(Quiddity_Status_FreeFlag << iota)
	GroupAssociated_Status_Blocked
	GroupAssociated_Status_Muted

	GroupAssociated_Status_WaitToAcceptByAdmins
	GroupAssociated_Status_WaitToAcceptByUser
)
