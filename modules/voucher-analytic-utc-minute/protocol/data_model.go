/* For license and copyright information please see the LEGAL file in the code repository */

package vaudp

import (
	"memar/protocol"
	"memar/time/utc"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	Minute() utc.MinuteElapsed
	TotalIssued() uint64
	TotalIssuedAmount() protocol.MoneyAmount

	// protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
