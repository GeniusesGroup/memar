/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// StaffScore or staff grade
type StaffScore interface {
	StaffID() StaffUUID             //
	Score() uint64                  //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}
