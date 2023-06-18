/* For license and copyright information please see the LEGAL file in the code repository */

package unp

import (
	"libgo/protocol"

	org "org/modules/org/protocol"
	qsp "org/modules/quiddity-status/protocol"
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
// it is use in many other services like send email(email address), ...
type DataModel interface {
	UserID() up.UserUUID            //
	OrgID() org.OrgUUID             //
	Username() string               // It is not replace of user ID. It usually use to find user by their friends in more human friendly manner.
	Status() UserName_Status        //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

// UserName_Status indicate UserName record status
type UserName_Status qsp.Quiddity_Status

// UserName status
const (
	UserName_Status_Reserved = UserName_Status(qsp.Quiddity_Status_FreeFlag << iota)
)

/*
	Errors
*/

const (
// UserName_Error_ = "domain/username.protocol; type=error; name="
)
