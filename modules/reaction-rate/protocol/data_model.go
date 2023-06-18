/* For license and copyright information please see the LEGAL file in the code repository */

package rrp

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type ReactionRate interface {
	ReactionTo() [16]byte           // any domain.
	Rate() uint8                    //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
