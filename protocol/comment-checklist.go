/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// CommentChecklist indicate the domain record data fields.
type CommentChecklist interface {
	CommentID() CommentUUID //
	//
	Time() protocol.Time        // Save time
	RequestID() UserRequestUUID // user-request domain
}
