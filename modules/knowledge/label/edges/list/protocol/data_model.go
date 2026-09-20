/* For license and copyright information please see the LEGAL file in the code repository */

package list_p

import (
	module_p "org/modules/computer/module/protocol"
	graph_p "org/modules/storage/graph/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	graph_p.Field_RelationPriority
	// To indicate SecondaryNode UUID belongs to which domain
	module_p.Field_ModuleUUID
}
