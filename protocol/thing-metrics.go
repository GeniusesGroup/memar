/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// each metrics for a thing is immutable record and so use version mechanism to chain metrics for a device.
type Temperature interface {
	ThingID() ThingUUID
	Amount() int64
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}
