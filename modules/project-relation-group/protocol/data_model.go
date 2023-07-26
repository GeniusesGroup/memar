/* For license and copyright information please see the LEGAL file in the code repository */

package prgp

import (
	"memar/protocol"

	gp "org/modules/group/protocol"
	pp "org/modules/project/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ProjectID() pp.ProjectUUID
	GroupID() gp.GroupUUID
	ProjectGroupRelation() Type

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
