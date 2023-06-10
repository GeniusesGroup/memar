/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	"libgo/time/utc"
)

// VoucherAnalyticUtcMinute indicate the domain record data fields.
type VoucherAnalyticUtcMinute interface {
	Minute() utc.MinuteElapsed          //
	Issued() uint64                     // Total
	IssuedAmount() protocol.MoneyAmount // Total
	Time() protocol.Time                // save time
}

type VoucherAnalyticUtcMinute_StorageServices interface {
	Save(dm VoucherAnalyticUtcMinute) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(voucherID VoucherUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(voucherID VoucherUUID, vo protocol.VersionOffset) (dm VoucherAnalyticUtcMinute, nv protocol.NumberOfVersion, err protocol.Error)
}
