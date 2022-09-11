/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// PersonPassword indicate the domain record data fields.
// A person can decide to don't register password and deny authenticate by password.
type PersonPassword interface {
	PersonID() protocol.UserID     // user domain
	PasswordHash() []byte          //
	Status() PersonPassword_Status //
	RequestID() UserRequestUUID    // user-request domain
}

type PersonPassword_StorageServices interface {
	Save(pp PersonPassword) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(personID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(personID [16]byte, vo protocol.VersionOffset) (pp PersonPassword, nv protocol.NumberOfVersion, err protocol.Error)
}

// PersonPassword_Status indicate PersonPassword record status
type PersonPassword_Status Quiddity_Status

// PersonPassword statuses
const (
	// authenticate person with Password + OTP
	PersonPassword_Status_ForceUse2Factor = PersonPassword_Status(Quiddity_Status_FreeFlag << iota)
	// user must change password and otp key(if enabled) for some reason
	PersonPassword_Status_MustChangePassword
	// user can't use or decide to prevent authenticate via password with or without OTP.
	PersonPassword_Status_DenyPasswordAuthentication
)

type PersonPassword_Service_SendResetToken_Request interface {
	How() uint8 // sms, email, ...
}
type PersonPassword_Service_SendResetToken_Response interface {
	Token() []byte // include Token&ExpireIn with signature by domain key.
}

type PersonPassword_Service_Register_Request interface {
	PasswordHash() []byte
}

type PersonPassword_Service_Confirm_Request interface {
	PersonID() protocol.UserID
	PasswordHash() []byte
}
type PersonPassword_Service_Confirm_Response interface {
	Status() PersonPassword_Status
}
