/* For license and copyright information please see the LEGAL file in the code repository */

package qrq_p

import (
	audit_p "org/modules/computer/audit/protocol"
	quiddity_p "org/modules/identity/quiddity/protocol"
	label_p "org/modules/knowledge/label/protocol"
	graph_p "org/modules/storage/graph/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	// Edge indicate relation reason e.g. Complement, Substitute, ...
	graph_p.DataModel[quiddity_p.UUID, quiddity_p.UUID, label_p.UUID]
	graph_p.Field_RelationPriority
	graph_p.Field_RelationDesirability
	Field_Status

	audit_p.Field_RequestID
	storage_p.Field_SaveTime
}
