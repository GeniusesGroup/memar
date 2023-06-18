/* For license and copyright information please see the LEGAL file in the code repository */

package ivaump

import (
	"libgo/protocol"
	"libgo/time/utc"
)

// InvoiceVoucherAnalyticUtcMinute indicate the domain record data fields.
type DataModel interface {
	Minute() utc.MinuteElapsed            //
	Redeemed() uint64                     // Total
	RedeemedAmount() protocol.MoneyAmount // Total
	SaveTime() protocol.Time              //
}


