/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// InviteRequestConfirmation indicate the domain record data fields.
type InviteRequestConfirmation interface {
	InviteID() InviteUUID                     //
	AccepterID() up.UserUUID                  //
	Status() InviteRequestConfirmation_Status //
	Time() protocol.Time                      // save time
	RequestID() urp.UserRequestUUID           //
}

type InviteRequestConfirmation_Status uint8

const (
	InviteRequestConfirmation_Status_Unset    InviteRequestConfirmation_Status = iota
	InviteRequestConfirmation_Status_OnHold                                    // GUI base
	InviteRequestConfirmation_Status_Accepted                                  //
	InviteRequestConfirmation_Status_Rejected                                  //
	InviteRequestConfirmation_Status_Expired                                   // GUI base
)
