/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// QuestionnaireQuestionRelation indicate the domain record data fields.
type QuestionnaireQuestionRelation interface {
	QuestionnaireID() QuestionnaireUUID       //
	QuestionID() QuestionUUID                 //
	Significance_Positive() uint64            //
	Significance_Negative() uint64            //
	Type() QuestionnaireQuestionRelation_Type //
	Time() protocol.Time                      // Save time
	RequestID() urp.UserRequestUUID           //
}

type QuestionnaireQuestionRelation_StorageServices interface {
	Save(pc QuestionnaireQuestionRelation) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(questionID QuestionUUID, questionnaireID QuestionnaireUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(questionID QuestionUUID, questionnaireID QuestionnaireUUID, vo protocol.VersionOffset) (pc QuestionnaireQuestionRelation, nv protocol.NumberOfVersion, err protocol.Error)
}

type QuestionnaireQuestionRelation_Type uint8

// TODO::: need types?
