/* For license and copyright information please see the LEGAL file in the code repository */

package bp

import (
	"memar/protocol"

	org "org/modules/org/protocol"
)

// TODO::: move all budget to the base domain

// Budget indicate the domain record data fields.
type DataModel interface {
	BudgetID() BudgetUUID
	OrgID() org.OrgUUID
	Type() Type

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
