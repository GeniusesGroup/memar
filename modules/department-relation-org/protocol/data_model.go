/* For license and copyright information please see the LEGAL file in the code repository */

package drop

import (
	"memar/protocol"

	dp "org/modules/department/protocol"
	org "org/modules/org/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	OwnerID() org.OrgUUID
	DepartmentID() dp.DepartmentUUID

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
