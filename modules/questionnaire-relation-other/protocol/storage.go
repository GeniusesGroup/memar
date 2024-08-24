/* For license and copyright information please see the LEGAL file in the code repository */

package qrop

import (
	"memar/protocol"

	qp "org/modules/questionnaire/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(questionnaireID qp.QuestionnaireUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(questionnaireID qp.QuestionnaireUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)
}
