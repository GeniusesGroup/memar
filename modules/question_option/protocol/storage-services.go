/* For license and copyright information please see the LEGAL file in the code repository */

package qop

import (
	"memar/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(questionOptionID QuestionOptionUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(questionOptionID QuestionOptionUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FILTER_QuestionOptionIDs_BY_Type(t Type, offset, limit uint64) (questionOptionIDs []QuestionOptionUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
