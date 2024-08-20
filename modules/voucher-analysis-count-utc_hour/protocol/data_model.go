/* For license and copyright information please see the LEGAL file in the code repository */

package vacuh

import (
	"memar/time/utc"

	aap "org/modules/app-audit/protocol"
	fmp "org/modules/financial-money/protocol"
	sp "org/modules/storage/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	Hour() utc.HourElapsed
	TotalIssued() uint64
	TotalIssuedAmount() fmp.MoneyAmount

	aap.AuditRequest
	sp.SaveTime
}
