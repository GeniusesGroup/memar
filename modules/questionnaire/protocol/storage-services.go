/* For license and copyright information please see the LEGAL file in the code repository */

package qp

import (
	"libgo/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(questionnaireID QuestionnaireUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(questionnaireID QuestionnaireUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_QuestionnaireIDs_By_Type(questionnaireID QuestionnaireUUID, t Type, offset, limit uint64) (nv protocol.NumberOfVersion, err protocol.Error)
}
