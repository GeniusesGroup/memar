/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// UserPublicKey indicate the domain record data fields.
type UserPublicKey interface {
	UserID() UserUUID               //
	PublicKey() []byte              // suggest use DER format
	Issuer() OrgUUID                //Use to get notify about status of the PK e.g. revoked notification, ...
	Status() UserPublicKey_Status   //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

// UserPublicKey_Status use to indicate UserPublicKey record status
type UserPublicKey_Status uint8

// UserPublicKey status
const (
	UserPublicKey_Status_Unset UserPublicKey_Status = iota
	UserPublicKey_Status_Active
	UserPublicKey_Status_Inactive
	UserPublicKey_Status_Blocked
	UserPublicKey_Status_Revoked
)
