/* For license and copyright information please see the LEGAL file in the code repository */

package qcu_p

import (
	request_p "memar/audit/request/protocol"
	audit_time_p "memar/audit/time/protocol"

	quiddity_p "org/modules/identity/quiddity/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	quiddity_p.Field_QuiddityID
	Field_CountUnitID
	// TODO::: Allow or need multiple count unit?

	request_p.Field_RequestID
	audit_time_p.Field_SaveTime
}
