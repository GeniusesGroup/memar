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
	Save(dm QuestionnaireQuestionRelation) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(questionnaireID QuestionnaireUUID, questionID QuestionUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(questionnaireID QuestionnaireUUID, questionID QuestionUUID, vo protocol.VersionOffset) (dm QuestionnaireQuestionRelation, nv protocol.NumberOfVersion, err protocol.Error)
}

type QuestionnaireQuestionRelation_Type uint8

// TODO::: need types?

// LIST_QuestionIDs_BY_QuestionnaireID(questionnaireID QuestionnaireUUID, offset, limit uint64) (questionIDs []QuestionUUID, nv protocol.NumberOfVersion, err protocol.Error)
