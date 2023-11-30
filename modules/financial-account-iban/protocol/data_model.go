/* For license and copyright information please see the LEGAL file in the code repository */

package faip

import (
	"memar/iso"
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	fap "org/modules/financial-account/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	AccountID() fap.FinancialAccountUUID
	IBAN() iso.IBAN

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
