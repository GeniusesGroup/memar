/* For license and copyright information please see the LEGAL file in the code repository */

package rrs_p

import (
	request_p "memar/audit/request/protocol"
	audit_time_p "memar/audit/time/protocol"

	datatype_p "org/modules/computer/type/protocol"
	rule_p "org/modules/organization/rule/protocol"
)

// DataModel indicate the domain record data fields.
//
// Other Frameworks:
// https://developers.cloudflare.com/ruleset-engine/about/phases/
type DataModel interface {
	rule_p.Field_RuleID

	// Entry point of the rule to execute
	// Rule engine Will execute rule when this data-type event will dispatched.
	datatype_p.Field_DataTypeID

	request_p.Field_RequestID
	audit_time_p.Field_SaveTime
}
