/* For license and copyright information please see the LEGAL file in the code repository */

package rc_p

import (
	request_p "memar/audit/request/protocol"
	audit_time_p "memar/audit/time/protocol"

	rule_p "org/modules/organization/rule/protocol"
	object_p "org/modules/storage/object/protocol"
)

// Use to store executable logic on portable binaries like WASM, ...
// Logic (any statement) CAN write in general purpose language or DSLs.
type DataModel interface {
	rule_p.Field_RuleID
	object_p.Field_ObjectID

	request_p.Field_RequestID
	audit_time_p.Field_SaveTime
}
