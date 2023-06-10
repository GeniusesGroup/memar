/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	"libgo/time/utc"
)

// VoucherAnalyticUtcDay indicate the domain record data fields.
type VoucherAnalyticUtcDay interface {
	Day() utc.DayElapsed                //
	Issued() uint64                     // Total
	IssuedAmount() protocol.MoneyAmount // Total
	Time() protocol.Time                // save time
}

type VoucherAnalyticUtcDay_StorageServices interface {
	Save(dm VoucherAnalyticUtcDay) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(voucherID VoucherUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(voucherID VoucherUUID, vo protocol.VersionOffset) (dm VoucherAnalyticUtcDay, nv protocol.NumberOfVersion, err protocol.Error)
}
