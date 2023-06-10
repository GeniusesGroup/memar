/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// QuestionObject indicate the domain record data fields.
type QuestionObject interface {
	QuestionID() QuestionUUID           //
	MediaTypes() []protocol.MediaTypeID //
	SizeLimit() uint64                  //
	Time() protocol.Time                // Save time
	RequestID() urp.UserRequestUUID     //
}

type QuestionObject_StorageServices interface {
	Save(dm QuestionObject) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(questionID QuestionUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(questionID QuestionUUID, vo protocol.VersionOffset) (dm QuestionObject, nv protocol.NumberOfVersion, err protocol.Error)
}
