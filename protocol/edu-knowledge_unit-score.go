/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// EducationKnowledgeUnitScore indicate the domain record data fields.
type EducationKnowledgeUnitScore interface {
	UserID() protocol.UserID                     //
	KnowledgeUnitID() EducationKnowledgeUnitUUID //
	GivenScoreID() protocol.UserID               //
	Duration() protocol.Duration                 // time duration to learn
	Score() uint64                               //
	Time() protocol.Time                         // save time
	RequestID() UserRequestUUID                  // user-request domain
}
