/* For license and copyright information please see the LEGAL file in the code repository */

package sip

import (
	"memar/protocol"

	sp "org/modules/staff/protocol"
)

type DataModel interface {
	StaffID() sp.StaffUUID

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
