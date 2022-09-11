/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

type ReactionRate interface {
	RelatedID() [16]byte        // any domain.
	Rate() uint8                //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}
