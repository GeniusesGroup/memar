/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// QuestionQuestionRelation indicate the domain record data fields.
type QuestionQuestionRelation interface {
	QuestionID() QuestionUUID            //
	RelationID() QuestionUUID            //
	Type() QuestionQuestionRelation_Type //
	Time() protocol.Time                 // Save time
	RequestID() urp.UserRequestUUID      // user-request domain
}

type QuestionQuestionRelation_Type uint8

const (
	QuestionQuestionRelation_Type_Unset QuestionQuestionRelation_Type = iota
	QuestionQuestionRelation_Type_SubQuestion
)
