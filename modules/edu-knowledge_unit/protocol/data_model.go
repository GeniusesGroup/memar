/* For license and copyright information please see the LEGAL file in the code repository */

package ekup

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	KnowledgeUnitID() EducationKnowledgeUnitUUID //
	UserID() up.UserUUID                         //
	Type() Type                                  // education unit type
	SaveTime() protocol.Time                     //
	RequestID() urp.UserRequestUUID              //
}

type Type uint32

// ?? > science > field > course > lessons > topics > ??
const (
	Type_Unset Type = 0

	// the state of knowing : knowledge as distinguished from ignorance or misunderstanding
	Type_Science Type = iota

	// a branch of knowledge
	Type_Field

	// education imparted in a series of lessons or meetings
	Type_Course

	Type_Lesson
	Type_Topic
)
