/* For license and copyright information please see the LEGAL file in the code repository */

package muap

import (
	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"

	utm_p "org/modules/forms/marketing/utm/protocol"
	user_p "org/modules/identity/user/protocol"
)

// Urchin Tracking Module (UTM) parameters
// https://en.wikipedia.org/wiki/UTM_parameters
type DataModel interface {
	utm_p.Field_UtmID
	user_p.Field_UserUUID

	utm_p.MarketingUTM

	request_p.Field_RequestID
	audit_time_p.Field_Request
}
