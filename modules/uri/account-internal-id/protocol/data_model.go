/* For license and copyright information please see the LEGAL file in the code repository */

package fai

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	fap "org/modules/financial-account/protocol"
)

// DataModel indicate the domain record data fields.
// It is about settlement reference internal ID like bank account ID.
type DataModel interface {
	AccountID() fap.FinancialAccountUUID
	ID() ID

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
