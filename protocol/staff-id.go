/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// TODO::: user-number??
type StaffID interface {
	StaffID() StaffUUID             //
	ID() uint32                     //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}
