/* For license and copyright information please see the LEGAL file in the code repository */

package usp

import (
	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"

	user_p "org/modules/identity/user/protocol"
)

type DataModel interface {
	ID() ID
	URI() string // e.g. UUID of picture object.
	user_p.Field_UserUUID

	request_p.Field_RequestID
	audit_time_p.Field_Request
}

const shortenerPath = "/s"
