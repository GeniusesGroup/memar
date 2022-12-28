/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// EducationKnowledgeUnitSelfStatement indicate the domain record data fields.
type EducationKnowledgeUnitSelfStatement interface {
	UserID() protocol.UserID                     //
	KnowledgeUnitID() EducationKnowledgeUnitUUID //
	// Language()
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}
