/* For license and copyright information please see the LEGAL file in the code repository */

package qmcp

import (
	"memar/protocol"

	qop "org/modules/question_option/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(questionOptionID qop.QuestionOptionUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(questionOptionID qop.QuestionOptionUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)
}
