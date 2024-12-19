/* For license and copyright information please see the LEGAL file in the code repository */

package rule_p

import (
	request_p "memar/audit/request/protocol"
	audit_time_p "memar/audit/time/protocol"

	node_p "org/modules/computer/node/protocol"
	label_p "org/modules/knowledge/label/protocol"
)

type DataModel interface {
	Field_RuleID
	Field_Type

	// TODO::: below fields are rule codes?? or belong to here?? or other subdomain?

	// `logic_p.Empty() == true` means rule not limit to any specific node
	node_p.Field_NodeID

	// `logic_p.Empty() == true` means rule not limit to any group of nodes with this label
	label_p.Field_LabelID

	request_p.Field_RequestID
	audit_time_p.Field_SaveTime
}
