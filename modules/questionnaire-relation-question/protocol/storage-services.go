/* For license and copyright information please see the LEGAL file in the code repository */

package qrqp

import (
	"memar/protocol"

	qp "org/modules/question/protocol"
	qrp "org/modules/questionnaire/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(questionnaireID qrp.QuestionnaireUUID, questionID qp.QuestionUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(questionnaireID qrp.QuestionnaireUUID, questionID qp.QuestionUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)
}
