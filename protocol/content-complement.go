/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type ContentComplement interface {
	ContentID() ContentUUID         //
	Priority() uint64               // complement priority
	ComplementID() ContentUUID      //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}
