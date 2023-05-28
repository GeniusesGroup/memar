/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// QuestionMultipleChoice indicate the domain record data fields.
type QuestionMultipleChoice interface {
	QuestionID() QuestionUUID       //
	Min() uint64                    //
	Max() uint64                    //
	Time() protocol.Time            // Save time
	RequestID() urp.UserRequestUUID //
}

type QuestionOptionMultipleChoice_StorageServices interface {
	Save(f QuestionMultipleChoice) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(questionOptionID QuestionOptionUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(questionOptionID QuestionOptionUUID, vo protocol.VersionOffset) (f QuestionMultipleChoice, nv protocol.NumberOfVersion, err protocol.Error)
}
