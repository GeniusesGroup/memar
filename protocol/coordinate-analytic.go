/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

type CoordinateAnalytic interface {
	CoordinateID() [16]byte     // quiddity||user||invoice||area||building||building-location||staff||... domain
	Distance() uint64           // km or ...
	AverageSpeed() uint64       // km/h or ...
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}
