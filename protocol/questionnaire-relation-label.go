/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// QuestionnaireLabel indicate the domain record data fields.
type QuestionnaireLabel interface {
	QuestionnaireID() QuestionnaireUUID //
	Label() LabelUUID                   //
	Time() protocol.Time                // Save time
	RequestID() urp.UserRequestUUID     //
}

type QuestionnaireLabel_StorageServices interface {
	Save(dm QuestionnaireLabel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(questionnaireID QuestionnaireUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(questionnaireID QuestionnaireUUID, vo protocol.VersionOffset) (dm QuestionnaireLabel, nv protocol.NumberOfVersion, err protocol.Error)
}
