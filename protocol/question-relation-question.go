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

type QuestionQuestionRelation_StorageServices interface {
	Save(f QuestionQuestionRelation) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(questionID QuestionUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(questionID QuestionUUID, vo protocol.VersionOffset) (f QuestionQuestionRelation, nv protocol.NumberOfVersion, err protocol.Error)

	ListAllQuestionRelations(questionID QuestionUUID, offset, limit uint64) (relationID []QuestionUUID, nv protocol.NumberOfVersion, err protocol.Error)
	FindByRelationID(relationID QuestionUUID, offset, limit uint64) (questionID []QuestionUUID, nv protocol.NumberOfVersion, err protocol.Error)
	FilterByType(questionID QuestionUUID, t QuestionQuestionRelation_Type, offset, limit uint64) (questionIDs []QuestionUUID, nv protocol.NumberOfVersion, err protocol.Error)

}

type QuestionQuestionRelation_Type uint8

const (
	QuestionQuestionRelation_Type_Unset QuestionQuestionRelation_Type = iota
	QuestionQuestionRelation_Type_SubQuestion
	QuestionQuestionRelation_Type_Translated
	QuestionQuestionRelation_Type_Complement
	QuestionQuestionRelation_Type_Hint // use for options not descriptive type.
)
