/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type CoordinateAnalytic interface {
	CoordinateID() CoordinateUUID   //
	Distance() uint64               // km or ...
	AverageSpeed() uint64           // km/h or ...
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}
