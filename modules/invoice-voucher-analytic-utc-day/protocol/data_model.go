/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	"libgo/time/utc"
)

// InvoiceVoucherAnalyticUtcDay indicate the domain record data fields.
type InvoiceVoucherAnalyticUtcDay interface {
	Day() utc.DayElapsed                  //
	Redeemed() uint64                     // Total
	RedeemedAmount() protocol.MoneyAmount // Total
	Time() protocol.Time                  // save time
}

type InvoiceVoucherAnalyticUtcDay_StorageServices interface {
	Save(dm InvoiceVoucherAnalyticUtcDay) (nv protocol.NumberOfVersion, err protocol.Error)

	Count() (nv protocol.NumberOfVersion, err protocol.Error)
	Get(vo protocol.VersionOffset) (dm InvoiceVoucherAnalyticUtcDay, nv protocol.NumberOfVersion, err protocol.Error)
}