/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	cp "org/modules/coordinate/protocol"
	urp "org/modules/user-request/protocol"
)

type DataModel interface {
	CoordinateID() cp.CoordinateUUID //
	Distance() uint64                // km or ...
	AverageSpeed() uint64            // km/h or ...
	SaveTime() protocol.Time         //
	RequestID() urp.UserRequestUUID  //
}
