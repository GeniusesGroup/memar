/* For license and copyright information please see the LEGAL file in the code repository */

package dsp

import (
	"memar/protocol"

	dp "org/modules/department/protocol"
)

type DepartmentStatus interface {
	DepartmentID() dp.DepartmentUUID
	Status() Status

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
