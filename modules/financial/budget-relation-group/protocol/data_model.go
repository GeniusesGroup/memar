/* For license and copyright information please see the LEGAL file in the code repository */

package brgp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	bp "org/modules/budget/protocol"
	gp "org/modules/group/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	BudgetID() bp.BudgetUUID
	GroupID() gp.GroupUUID

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
