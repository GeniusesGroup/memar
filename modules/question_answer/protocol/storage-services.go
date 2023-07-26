/* For license and copyright information please see the LEGAL file in the code repository */

package qap

import (
	"memar/protocol"

	up "org/modules/user/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(answerID AnswerUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(answerID AnswerUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	// shall I pass questionID as well ??
	LIST_RespondentIDs_BY_AnswerID(answerID AnswerUUID, offset, limit uint64) (answerBys []up.UserUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
