/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	"libgo/time/earth"
	"libgo/time/utc"
	urp "org/modules/user-request/protocol"
)

// DiscountTimingUTC indicate the domain record data fields.
type DiscountTimingUTC interface {
	DiscountID() DiscountUUID       //
	Weekdays() utc.Weekdays         // what days in weekday in utc time week allow to use this discount
	DayHours() earth.DayHours       // what hours in day in utc time week allow to use this discount
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type DiscountTimingUTC_StorageServices interface {
	Save(dt DiscountTimingUTC) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(discountID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(discountID [16]byte, vo protocol.VersionOffset) (dt DiscountTimingUTC, nv protocol.NumberOfVersion, err protocol.Error)
}
