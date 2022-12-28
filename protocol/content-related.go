/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

type ContentRelated interface {
	ContentID() ContentUUID     // content domain
	Priority() uint64           // substitute priority
	PriorityType() [16]byte     // type domain
	RelatedID() ContentUUID     // content domain
	UserID() protocol.UserID    // user domain
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}
