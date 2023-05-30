/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	"libgo/time/earth"
	"libgo/time/utc"
	urp "org/modules/user-request/protocol"
)

type ProductTimingUTC interface {
	ProductID() ProductUUID         //
	Day() utc.DayElapsed            //
	DayHours() earth.DayHours       // what hours in a day this service active to provide services
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type ProductTimingUTC_StorageServices interface {
	Save(pt ProductTimingUTC) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID ProductUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID ProductUUID, vo protocol.VersionOffset) (pt ProductTimingUTC, nv protocol.NumberOfVersion, err protocol.Error)
}
