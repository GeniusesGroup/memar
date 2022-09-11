/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

type ContentRelated interface {
	ContentID() [16]byte        // content domain
	Priority() int32            // substitute priority
	PriorityType() [16]byte     // type domain
	RelatedID() [16]byte        // content domain
	UserID() protocol.UserID    // user domain
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}
