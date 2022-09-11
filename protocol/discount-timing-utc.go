/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
	"github.com/GeniusesGroup/libgo/time/earth"
	"github.com/GeniusesGroup/libgo/time/utc"
)

// DiscountTimingUTC indicate the domain record data fields.
type DiscountTimingUTC interface {
	DiscountID() [16]byte       // discount domain
	Weekdays() utc.Weekdays     // what days in weekday in utc time week allow to use this discount
	DayHours() earth.DayHours   // what hours in day in utc time week allow to use this discount
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type DiscountTimingUTC_StorageServices interface {
	Save(dt DiscountTimingUTC) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(discountID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(discountID [16]byte, vo protocol.VersionOffset) (dt DiscountTimingUTC, nv protocol.NumberOfVersion, err protocol.Error)
}
