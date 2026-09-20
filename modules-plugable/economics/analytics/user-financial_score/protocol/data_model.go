/* For license and copyright information please see the LEGAL file in the code repository */

package score_p

import (
	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"

	user_p "org/modules/identity/user/protocol"
)

// Individual and General score
type DataModel interface {
	user_p.Field_UserUUID

	FinancialScore() int64

	// Store user risk to prevent or detect frauds
	RiskScore() int64

	request_p.Field_RequestID
	audit_time_p.Field_Request
}
