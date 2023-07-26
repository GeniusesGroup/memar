/* For license and copyright information please see the LEGAL file in the code repository */

package qrp

import (
	"memar/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(questionnaireRespondentID QuestionnaireRespondentUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(questionnaireRespondentID QuestionnaireRespondentUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)
}
