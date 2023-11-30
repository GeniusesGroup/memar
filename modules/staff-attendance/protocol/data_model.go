/* For license and copyright information please see the LEGAL file in the code repository */

package sap

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	sp "org/modules/staff/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	StaffID() sp.StaffUUID
	Type() Type

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
