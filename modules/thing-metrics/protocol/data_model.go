/* For license and copyright information please see the LEGAL file in the code repository */

package tmp

import (
	"libgo/protocol"

	tp "org/modules/thing/protocol"
	urp "org/modules/user-request/protocol"
)

// each metrics for a thing is immutable record and so use version mechanism to chain metrics for a device.
type DataModel interface {
	ThingID() tp.ThingUUID
	Amount() int64
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
