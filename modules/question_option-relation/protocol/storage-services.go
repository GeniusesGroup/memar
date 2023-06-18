/* For license and copyright information please see the LEGAL file in the code repository */

package qorp

import (
	"libgo/protocol"

	qop "org/modules/question_option/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(questionOptionID qop.QuestionOptionUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(questionOptionID qop.QuestionOptionUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_QuestionOptionIDs_BY_RelationID(RelationID [16]byte, offset, limit uint64) (questionOptionIDs []qop.QuestionOptionUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_RelationIDs_BY_QuestionOptionID(questionOptionID qop.QuestionOptionUUID, offset, limit uint64) (relationIDs [16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}
