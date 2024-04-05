/* For license and copyright information please see the LEGAL file in the code repository */

package vacuh

import (
	"memar/protocol"
	"memar/time/utc"

	fmp "org/modules/financial-money/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	Hour() utc.HourElapsed
	TotalIssued() uint64
	TotalIssuedAmount() fmp.MoneyAmount

	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
