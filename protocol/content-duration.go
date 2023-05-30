/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// EducationKnowledgeUnitDuration indicate the domain record data fields.
type ContentDuration interface {
	KnowledgeUnitID() EducationKnowledgeUnitUUID //
	Duration() protocol.Duration                 // AI suggested duration
	Time() protocol.Time                         // save time
	RequestID() urp.UserRequestUUID              //
}
