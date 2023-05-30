/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// EducationKnowledgeUnitDuration indicate the domain record data fields.
type EducationKnowledgeUnitDuration interface {
	KnowledgeUnitID() EducationKnowledgeUnitUUID //
	Minimum() protocol.Duration                  // Minimum time duration to learn
	Expected() protocol.Duration                 // Expected time duration to learn
	Maximum() protocol.Duration                  // Maximum time duration to learn
	Time() protocol.Time                         // save time
	RequestID() urp.UserRequestUUID              //
}
