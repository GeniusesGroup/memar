/* For license and copyright information please see the LEGAL file in the code repository */

package un_p

import (
	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"

	org_p "org/modules/identity/organization/protocol"
	user_p "org/modules/identity/user/protocol"
)

// DataModel indicate the domain record data fields.
// it is use in many other services like send email(email address), ...
type DataModel interface {
	user_p.Field_UserUUID
	org_p.Field_OrganizationID
	Field_Username

	request_p.Field_RequestID
	audit_time_p.Field_Request
}
