/* For license and copyright information please see the LEGAL file in the code repository */

package contract_p

import (
	request_p "memar/audit/request/protocol"
	audit_time_p "memar/audit/time/protocol"
)

type DataModel interface {
	Field_ContractID
	Field_Terms
	Field_Data

	request_p.Field_RequestID
	audit_time_p.Field_SaveTime
}

// Service: fulfill the obligation
