/* For license and copyright information please see the LEGAL file in the code repository */

package qorqop

import (
	"libgo/protocol"

	qop "org/modules/question_option/protocol"
	urp "org/modules/user-request/protocol"
)

// In most cases just when Type_Criterion flag is on.

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionOptionID() qop.QuestionOptionUUID //
	RelationID() qop.QuestionOptionUUID       //
	// Type()
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
