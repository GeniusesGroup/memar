/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// QuiddityIcon indicate the domain record data fields.
// Icon or emoji use in many domains e.g. category, departments, ...
type QuiddityIcon interface {
	QuiddityID() QuiddityUUID       //
	Icon() ObjectUUID               //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}
