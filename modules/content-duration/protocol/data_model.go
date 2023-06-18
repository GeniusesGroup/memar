/* For license and copyright information please see the LEGAL file in the code repository */

package cdp

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	cp "org/modules/content/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ContentID() cp.ContentUUID
	Duration() protocol.Duration    // AI suggested duration
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}


