/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// EducationKnowledgeUnitScore indicate the domain record data fields.
type EducationKnowledgeUnitScore interface {
	UserID() up.UserUUID                         //
	KnowledgeUnitID() EducationKnowledgeUnitUUID //
	GivenScoreID() up.UserUUID                   //
	Duration() protocol.Duration                 // time duration to learn
	Score() uint64                               //
	Time() protocol.Time                         // save time
	RequestID() urp.UserRequestUUID              //
}
