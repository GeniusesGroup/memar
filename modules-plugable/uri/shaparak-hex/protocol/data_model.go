/* For license and copyright information please see the LEGAL file in the code repository */

package fcsp

import (
	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"

	card_p "org/modules/vertices/card/protocol"
)

// store users bank account to distinguish user balances in desire indexes
type DataModel interface {
	card_p.Field_CardID
	CardHexSHA1() CardHexSHA1

	request_p.Field_RequestID
	audit_time_p.Field_Request
}
