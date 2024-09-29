/* For license and copyright information please see the LEGAL file in the code repository */

package lro_p

import (
	audit_p "org/modules/computer/audit/protocol"
	module_p "org/modules/computer/module/protocol"
	user_p "org/modules/identity/user/protocol"
	label_p "org/modules/knowledge/label/protocol"
	graph_p "org/modules/storage/graph/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

// TODO::: Need this domain??

// DataModel indicate the domain record data fields.
type DataModel interface {
	// SecondaryNode can be any domain(Module) UUID usually product, content, ... domain
	// SecondaryNode can be also label to categorize labels too.
	graph_p.DataModel[label_p.UUID, storage_p.RecordUUID, user_p.UUID]

	graph_p.Field_RelationPriority
	// To indicate SecondaryNode UUID belongs to which domain
	module_p.Field_ModuleID
	Field_Status

	audit_p.Field_RequestID
	storage_p.Field_SaveTime
}
