/* For license and copyright information please see the LEGAL file in the code repository */

package qru_p

import (
	audit_p "org/modules/computer/audit/protocol"
	quiddity_p "org/modules/identity/quiddity/protocol"
	user_p "org/modules/identity/user/protocol"
	label_p "org/modules/knowledge/label/protocol"
	graph_p "org/modules/storage/graph/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	// Edge indicate `RelationType`
	graph_p.DataModel[quiddity_p.UUID, user_p.UUID, label_p.UUID]

	Status()

	audit_p.Field_RequestID
	storage_p.Field_SaveTime
}
