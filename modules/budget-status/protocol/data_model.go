/* For license and copyright information please see the LEGAL file in the code repository */

package bsp

import (
	"memar/protocol"

	bp "org/modules/budget/protocol"
)

// TODO::: move all budget to the base domain

// DataModel indicate the domain record data fields.
type DataModel interface {
	BudgetID() bp.BudgetUUID
	Status() Status

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
