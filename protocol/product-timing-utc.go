/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	"libgo/time/earth"
	"libgo/time/utc"
)

type ProductTimingUTC interface {
	ProductID() ProductUUID     //
	Day() utc.DayElapsed        //
	DayHours() earth.DayHours   // what hours in a day this service active to provide services
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type ProductTimingUTC_StorageServices interface {
	Save(pt ProductTimingUTC) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID [16]byte, vo protocol.VersionOffset) (pt ProductTimingUTC, nv protocol.NumberOfVersion, err protocol.Error)
}
