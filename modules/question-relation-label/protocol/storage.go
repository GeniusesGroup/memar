/* For license and copyright information please see the LEGAL file in the code repository */

package qrlp

import (
	"memar/protocol"

	lp "org/modules/label/protocol"
	qp "org/modules/question/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(questionID qp.QuestionUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(questionID qp.QuestionUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_QuestionIDs_BY_LabelID(labelID lp.LabelUUID, offset, limit uint64) (questionIDs []qp.QuestionUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_LabelIDs_BY_QuestionID(questionID qp.QuestionUUID, offset, limit uint64) (labelIDs []lp.LabelUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
