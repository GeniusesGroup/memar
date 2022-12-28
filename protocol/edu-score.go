/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// EducationScore indicate the domain record data fields.
type EducationScore interface {
	OrgID() [16]byte            //
	UserID() protocol.UserID    //
	Score() uint64              //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}
