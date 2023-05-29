/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type StaffInterview interface {
	StaffID() StaffUUID //

	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}
