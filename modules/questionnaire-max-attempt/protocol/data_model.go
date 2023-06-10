/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// QuestionnaireMaxAttempt indicate the domain record data fields.
type QuestionnaireMaxAttempt interface {
	QuestionnaireID() QuestionnaireUUID //
	MaxAttempt() uint16                 //
	Time() protocol.Time                // Save time
	RequestID() urp.UserRequestUUID     //
}

type QuestionnaireMaxAttempt_StorageServices interface {
	Save(dm QuestionnaireMaxAttempt) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(questionnaireID QuestionnaireUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(questionnaireID QuestionnaireUUID, vo protocol.VersionOffset) (dm QuestionnaireMaxAttempt, nv protocol.NumberOfVersion, err protocol.Error)
}
