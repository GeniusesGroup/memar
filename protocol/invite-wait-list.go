/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// InviteWaitList indicate the domain record data fields.
type InviteWaitList interface {
	InviteID() InviteUUID          //
	ConsumerID() protocol.UserID   // user domain
	Status() InviteWaitList_Status //
	Time() protocol.Time           // save time
	RequestID() UserRequestUUID    // user-request domain
}

type InviteWaitList_Status uint8

const (
	InviteWaitList_Status_Unset     InviteWaitList_Status = iota
	InviteWaitList_Status_Wait                            // GUI base
	InviteWaitList_Status_Confirmed                       //
	InviteWaitList_Status_Canceled                        //
	InviteWaitList_Status_Expired                         // GUI base
)
