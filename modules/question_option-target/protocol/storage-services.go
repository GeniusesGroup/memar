/* For license and copyright information please see the LEGAL file in the code repository */

package qotp

import (
	"libgo/protocol"

	qp "org/modules/question/protocol"
	urp "org/modules/user-request/protocol"
	qop "org/modules/question_option/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(questionOptionID qp.QuestionUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(questionOptionID qp.QuestionUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)
}
