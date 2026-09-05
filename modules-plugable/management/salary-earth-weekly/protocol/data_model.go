/* For license and copyright information please see the LEGAL file in the code repository */

package ssp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	sp "org/modules/staff/protocol"
)

// DataModel is fixed negotiated salary that don't follow org||department||role salary rules.
type DataModel interface {
	StaffID() sp.StaffUUID
	WeeklySalary() protocol.MoneyAmount

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
