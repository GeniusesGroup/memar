/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// It is announcement that user tell the system to start answer to questions.

// QuestionnaireRespondentTaskRelation indicate the domain record data fields.
type QuestionnaireRespondentTaskRelation interface {
	QuestionnaireRespondentID() QuestionnaireRespondentUUID //
	TaskID() TaskUUID                                       //
	Type() QuestionnaireRespondentTaskRelation_Type         //
	Time() protocol.Time                                    // save time
	RequestID() urp.UserRequestUUID                         //
}

type QuestionnaireRespondentTaskRelation_Type uint8

const (
	QuestionnaireRespondentTaskRelation_Type_Unset QuestionnaireRespondentTaskRelation_Type = iota
	QuestionnaireRespondentTaskRelation_Type_Creator
	QuestionnaireRespondentTaskRelation_Type_Pending
)
