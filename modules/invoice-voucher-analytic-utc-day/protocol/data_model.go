/* For license and copyright information please see the LEGAL file in the code repository */

package ivaudp

import (
	"memar/protocol"
	"memar/time/utc"
	// arp "org/modules/app-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	Day() utc.DayElapsed
	TotalRedeemed() uint64
	TotalRedeemedAmount() protocol.MoneyAmount

	// arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
