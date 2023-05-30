/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// EducationKnowledgeUnitSelfStatement indicate the domain record data fields.
type EducationKnowledgeUnitSelfStatement interface {
	UserID() UserUUID                            //
	KnowledgeUnitID() EducationKnowledgeUnitUUID //
	// Language()
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}
