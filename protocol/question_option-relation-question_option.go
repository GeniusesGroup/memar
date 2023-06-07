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
	// Type()
	Time() protocol.Time            // Save time
	RequestID() urp.UserRequestUUID //
}

type QuestionOptionQuestionOptionRelation_StorageServices interface {
	Save(dm QuestionOptionQuestionOptionRelation) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(questionOptionID QuestionUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(questionOptionID QuestionUUID, vo protocol.VersionOffset) (dm QuestionOptionQuestionOptionRelation, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_QuestionOptionIDs_BY_RelationID(relationID QuestionOptionUUID, offset, limit uint64) (questionOptionID []QuestionOptionUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_RelationIDs_BY_QuestionOptionID(questionOptionID QuestionOptionUUID, offset, limit uint64) (relationIDs []QuestionOptionUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
