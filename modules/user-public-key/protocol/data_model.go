/* For license and copyright information please see the LEGAL file in the code repository */

package upkp

import (
	"libgo/protocol"

	org "org/modules/org/protocol"
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	UserID() up.UserUUID            //
	PublicKey() []byte              // suggest use DER format
	Issuer() org.OrgUUID            //Use to get notify about status of the PK e.g. revoked notification, ...
	Status() Status                 //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

// Status use to indicate UserPublicKey record status
type Status uint8

// UserPublicKey status
const (
	Status_Unset Status = iota
	Status_Active
	Status_Inactive
	Status_Blocked
	Status_Revoked
)
