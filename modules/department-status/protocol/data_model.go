/* For license and copyright information please see the LEGAL file in the code repository */

package dsp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	dp "org/modules/department/protocol"
)

type DepartmentStatus interface {
	DepartmentID() dp.DepartmentUUID
	Status() Status

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
