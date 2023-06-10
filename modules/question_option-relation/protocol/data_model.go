/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// QuestionOption indicate the domain record data fields.
type QuestionOptionRelation interface {
	QuestionOptionID() QuestionOptionUUID //
	RelationID() [16]byte                 // Question, Questionnaire
	Time() protocol.Time                  // Save time
	RequestID() urp.UserRequestUUID       //
}

type QuestionOptionRelation_StorageServices interface {
	Save(dm QuestionOptionRelation) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(questionOptionID QuestionOptionUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(questionOptionID QuestionOptionUUID, vo protocol.VersionOffset) (dm QuestionOptionRelation, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_QuestionOptionIDs_BY_RelationID(RelationID [16]byte, offset, limit uint64) (questionOptionIDs []QuestionOptionUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_RelationIDs_BY_QuestionOptionID(questionOptionID QuestionOptionUUID, offset, limit uint64) (relationIDs [16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}
