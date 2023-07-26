/* For license and copyright information please see the LEGAL file in the code repository */

package dp

import (
	"memar/protocol"
)

// DataModel indicate the domain record data fields.
// It can use to show organizational chart. Also staffs can join to the related group.
type DataModel interface {
	DepartmentID() DepartmentUUID
	ParentID() DepartmentUUID // Exist if it isn't top of the organization.

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
