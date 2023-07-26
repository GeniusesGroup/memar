/* For license and copyright information please see the LEGAL file in the code repository */

package ivaump

import (
	"memar/protocol"
	"memar/time/utc"
)

// InvoiceVoucherAnalyticUtcMinute indicate the domain record data fields.
type DataModel interface {
	Minute() utc.MinuteElapsed
	TotalRedeemed() uint64
	TotalRedeemedAmount() protocol.MoneyAmount

	// protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
