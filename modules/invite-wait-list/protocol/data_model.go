/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// InviteWaitList indicate the domain record data fields.
type InviteWaitList interface {
	InviteID() InviteUUID           //
	ConsumerID() up.UserUUID        //
	Status() InviteWaitList_Status  //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type InviteWaitList_Status uint8

const (
	InviteWaitList_Status_Unset     InviteWaitList_Status = iota
	InviteWaitList_Status_Wait                            // GUI base
	InviteWaitList_Status_Confirmed                       //
	InviteWaitList_Status_Canceled                        //
	InviteWaitList_Status_Expired                         // GUI base
)
