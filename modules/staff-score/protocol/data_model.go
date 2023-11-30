/* For license and copyright information please see the LEGAL file in the code repository */

package ssp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	sp "org/modules/staff/protocol"
)

// DataModel or staff grade
type DataModel interface {
	StaffID() sp.StaffUUID
	Score() uint64

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
