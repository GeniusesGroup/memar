/* For license and copyright information please see the LEGAL file in the code repository */

package rsp

import (
	"memar/protocol"

	rp "org/modules/role/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	RoleID() rp.RoleUUID
	Minimum() int32  // Minimum number of employees for this job position
	Expected() int32 // Expected number of employees for this job position
	Maximum() int32  // Maximum number of employees for this job position

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
