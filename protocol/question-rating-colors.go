/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// QuestionRatingColors indicate the domain record data fields.
type QuestionRatingColors interface {
	QuestionID() QuestionUUID       //
	Colors() []protocol.RGB         //
	Time() protocol.Time            // Save time
	RequestID() urp.UserRequestUUID // user-request domain
}

type  QuestionRatingColors_StorageServices interface {
	Save(f QuestionRatingColors) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(questionID QuestionUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(questionID QuestionUUID, vo protocol.VersionOffset) (f QuestionRatingColors, nv protocol.NumberOfVersion, err protocol.Error)

}

