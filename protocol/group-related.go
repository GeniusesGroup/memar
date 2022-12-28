/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// GroupRelated indicate the domain record data fields.
type GroupRelated interface {
	GroupID() [16]byte          // group domain
	RelatedGroupID() [16]byte   // group domain. Use to categorize and graph groups
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}
