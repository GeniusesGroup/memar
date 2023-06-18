/* For license and copyright information please see the LEGAL file in the code repository */

package qorqop

import (
	"libgo/protocol"

	qp "org/modules/question/protocol"
	qop "org/modules/question_option/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(questionOptionID qp.QuestionUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(questionOptionID qp.QuestionUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_QuestionOptionIDs_BY_RelationID(relationID qop.QuestionOptionUUID, offset, limit uint64) (questionOptionID []qop.QuestionOptionUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_RelationIDs_BY_QuestionOptionID(questionOptionID qop.QuestionOptionUUID, offset, limit uint64) (relationIDs []qop.QuestionOptionUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
