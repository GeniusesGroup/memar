/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

type EducationKnowledgeUnitUUID = protocol.UUID

// EducationKnowledgeUnit indicate the domain record data fields.
type EducationKnowledgeUnit interface {
	KnowledgeUnitID() EducationKnowledgeUnitUUID //
	UserID() up.UserUUID                         //
	Type() Education_Type                        // education unit type
	Time() protocol.Time                         // save time
	RequestID() urp.UserRequestUUID              //
}

type Education_Type uint32

// ?? > science > field > course > lessons > topics > ??
const (
	Education_Type_Unset Education_Type = 0

	// the state of knowing : knowledge as distinguished from ignorance or misunderstanding
	Education_Type_Science Education_Type = iota

	// a branch of knowledge
	Education_Type_Field

	// education imparted in a series of lessons or meetings
	Education_Type_Course

	Education_Type_Lesson
	Education_Type_Topic
)
