/* For license and copyright information please see the LEGAL file in the code repository */

package lro_p

import (
	request_p "memar/audit/request/protocol"
	audit_time_p "memar/audit/time/protocol"
	record_p "memar/storage/record/protocol"

	module_p "org/modules/computer/module/protocol"
	org_p "org/modules/identity/org/protocol"
	user_p "org/modules/identity/user/protocol"
	label_p "org/modules/knowledge/label/protocol"
	graph_p "org/modules/storage/graph/protocol"
)

// Some usage example:
// - label (Commodity) relate to Product (abc) by User (Omid)
// - label (Suggestion) relate to Task (123456) by User (Omid)

// DataModel indicate the domain record data fields.
type DataModel interface {
	// indicate labeling occur in which organization.
	org_p.Field_OrganizationID

	// SecondaryNode can be any domain(Module) UUID usually product, content, ... domain
	// SecondaryNode can be also label to categorize labels too.
	// Edge indicate who(person)||which(organization) relate the label to the record.
	graph_p.DataModel[label_p.UUID, record_p.UUID, user_p.UUID]

	graph_p.Field_RelationPriority
	// To indicate SecondaryNode UUID belongs to which domain
	module_p.Field_ModuleID
	Field_Status

	request_p.Field_RequestID
	audit_time_p.Field_SaveTime
}
