/* For license and copyright information please see the LEGAL file in the code repository */

package qafitbp

import (
	"libgo/protocol"
	qap "org/modules/question-answer/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(answerID qap.AnswerUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(answerID qap.AnswerUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)
}
