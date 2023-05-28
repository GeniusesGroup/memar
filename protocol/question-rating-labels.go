/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// QuestionRatingLabels indicate the domain record data fields.
type QuestionRatingLabels interface {
	QuestionID() QuestionUUID       //
	Labels() []QuiddityUUID         //
	Time() protocol.Time            // Save time
	RequestID() urp.UserRequestUUID //
}

type QuestionRatingLabels_StorageServices interface {
	Save(f QuestionRatingLabels) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(questionID QuestionUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(questionID QuestionUUID, vo protocol.VersionOffset) (f QuestionRatingLabels, nv protocol.NumberOfVersion, err protocol.Error)
}
