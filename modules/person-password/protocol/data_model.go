/* For license and copyright information please see the LEGAL file in the code repository */

package ppp

import (
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
// A person can decide to don't register password and deny authenticate by password.
type DataModel interface {
	PersonID() up.UserUUID
	PasswordHash() PasswordHash
	Status() Status
	RequestID() urp.UserRequestUUID
}
