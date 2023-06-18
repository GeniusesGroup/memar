/* For license and copyright information please see the LEGAL file in the code repository */

package ppp

import (
	qsp "org/modules/quiddity-status/protocol"
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
// A person can decide to don't register password and deny authenticate by password.
type DataModel interface {
	PersonID() up.UserUUID          //
	PasswordHash() []byte           //
	Status() Status                 //
	RequestID() urp.UserRequestUUID //
}

// Status indicate PersonPassword record status
type Status qsp.Quiddity_Status

// PersonPassword statuses
const (
	// authenticate person with Password + OTP
	Status_ForceUse2Factor = Status(qsp.Quiddity_Status_FreeFlag << iota)
	// user must change password and otp key(if enabled) for some reason
	Status_MustChangePassword
	// user can't use or decide to prevent authenticate via password with or without OTP.
	Status_DenyPasswordAuthentication
)
