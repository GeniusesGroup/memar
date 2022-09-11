/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
	"github.com/GeniusesGroup/libgo/time/utc"
)

// InvoiceVoucherAnalyticUtcMinute indicate the domain record data fields.
type InvoiceVoucherAnalyticUtcMinute interface {
	Minute() utc.MinuteElapsed            //
	Redeemed() uint64                     // Total
	RedeemedAmount() protocol.MoneyAmount // Total
	Time() protocol.Time                  // save time
}

type InvoiceVoucherAnalyticUtcMinute_StorageServices interface {
	Save(iva InvoiceVoucherAnalyticUtcMinute) (nv protocol.NumberOfVersion, err protocol.Error)

	Count() (nv protocol.NumberOfVersion, err protocol.Error)
	Get(vo protocol.VersionOffset) (iva InvoiceVoucherAnalyticUtcMinute, nv protocol.NumberOfVersion, err protocol.Error)
}
