/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// QuestionnaireStartPoint indicate the domain record data fields.
type QuestionnaireStartPoint interface {
	QuestionnaireID() QuestionnaireUUID //
	// TODO::: embed or copy??
	protocol.Time                   //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type QuestionnaireStartPoint_StorageServices interface {
	Save(pc QuestionnaireStartPoint) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(questionnaireID QuestionnaireUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(questionnaireID QuestionnaireUUID, vo protocol.VersionOffset) (pc QuestionnaireStartPoint, nv protocol.NumberOfVersion, err protocol.Error)
}
