/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// QuestionOptionMultipleChoice indicate the domain record data fields.
type QuestionOptionMultipleChoice interface {
	QuestionOptionID() QuestionOptionUUID //
	Min() uint64                          //
	Max() uint64                          //
	Time() protocol.Time                  // Save time
	RequestID() urp.UserRequestUUID       // user-request domain
}

type  QuestionOptionMultipleChoice_StorageServices interface {
	Save(f QuestionOptionMultipleChoice) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(questionOptionID QuestionOptionUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(questionOptionID QuestionOptionUUID, vo protocol.VersionOffset) (f QuestionOptionMultipleChoice, nv protocol.NumberOfVersion, err protocol.Error)

}
