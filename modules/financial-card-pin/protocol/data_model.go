/* For license and copyright information please see the LEGAL file in the code repository */

package dcpp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	fcp "org/modules/financial-card/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	FinancialCardID() fcp.FinancialCardUUID
	FixedPin1() uint32
	FixedPin2() uint32
	DynamicPin1() OTPKey
	DynamicPin2() OTPKey

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
