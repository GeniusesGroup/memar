/* For license and copyright information please see the LEGAL file in the code repository */

package qoop

import (
	"libgo/protocol"

	qp "org/modules/question/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(questionID qp.QuestionUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(questionID qp.QuestionUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)
}
