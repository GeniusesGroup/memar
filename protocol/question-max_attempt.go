/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// QuestionMaxAttempt indicate the domain record data fields.
type QuestionMaxAttempt interface {
	QuestionID() QuestionUUID       //
	MaxAttempt() uint16             //
	Time() protocol.Time            // Save time
	RequestID() urp.UserRequestUUID //
}

type QuestionMaxAttempt_StorageServices interface {
	Save(dm QuestionMaxAttempt) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(questionID QuestionUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(questionID QuestionUUID, vo protocol.VersionOffset) (dm QuestionMaxAttempt, nv protocol.NumberOfVersion, err protocol.Error)
}
