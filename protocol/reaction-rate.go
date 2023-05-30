/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type ReactionRate interface {
	ReactionTo() [16]byte           // any domain.
	Rate() uint8                    //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}
