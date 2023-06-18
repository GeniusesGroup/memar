/* For license and copyright information please see the LEGAL file in the code repository */

package qp

import (
	"libgo/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(questionID QuestionUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(questionID QuestionUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	// TODO::: a method to find all questions have quiz type??
	// FindByType(questionID QuestionUUID, t Type, offset, limit uint64) (questionIDs []QuestionUUID, nv protocol.NumberOfVersion, err protocol.Error)
	FILTER_QuestionIDs_BY_Type(t Type, offset, limit uint64) (questionIDs []QuestionUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
