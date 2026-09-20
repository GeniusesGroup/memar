/* For license and copyright information please see the LEGAL file in the code repository */

// use in risk assessment
package farap

import (
	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"

	account_p "org/modules/economics/account/protocol"
)

// DataModel
// Store user risk to prevent or detect frauds
type DataModel interface {
	account_p.Field_AccountID
	Score() int64

	request_p.Field_RequestID
	audit_time_p.Field_Request
}
