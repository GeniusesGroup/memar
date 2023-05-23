/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// In most cases just when QuestionOption_Type_Criterion flag is on.

// QuestionOptionQuestionOptionRelation indicate the domain record data fields.
type QuestionOptionQuestionOptionRelation interface {
	QuestionOptionID() QuestionOptionUUID //
	RelationID() QuestionOptionUUID       //
	Time() protocol.Time                  // Save time
	RequestID() urp.UserRequestUUID       // user-request domain
}
