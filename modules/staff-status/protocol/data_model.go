/* For license and copyright information please see the LEGAL file in the code repository */

package ssp

import (
	"memar/protocol"

	sp "org/modules/staff/protocol"
)

type DataModel interface {
	StaffID() sp.StaffUUID
	Status() Status

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
