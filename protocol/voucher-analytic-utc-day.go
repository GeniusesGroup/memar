/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
	"github.com/GeniusesGroup/libgo/time/utc"
)

// VoucherAnalyticUtcDay indicate the domain record data fields.
type VoucherAnalyticUtcDay interface {
	Day() utc.DayElapsed                //
	Issued() uint64                     // Total
	IssuedAmount() protocol.MoneyAmount // Total
	Time() protocol.Time                // save time
}

type VoucherAnalyticUtcDay_StorageServices interface {
	Save(va VoucherAnalyticUtcDay) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(voucherID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(voucherID [16]byte, vo protocol.VersionOffset) (va VoucherAnalyticUtcDay, nv protocol.NumberOfVersion, err protocol.Error)
}
