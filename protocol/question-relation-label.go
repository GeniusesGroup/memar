/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// QuestionLabelRelation indicate the domain record data fields.
type QuestionLabelRelation interface {
	QuestionID() QuestionUUID       //
	Label() LabelUUID               //
	Time() protocol.Time            // Save time
	RequestID() urp.UserRequestUUID // user-request domain
}

type QuestionLabelRelation_StorageServices interface {
	Save(f QuestionLabelRelation) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(questionID QuestionUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(questionID QuestionUUID, vo protocol.VersionOffset) (f QuestionLabelRelation, nv protocol.NumberOfVersion, err protocol.Error)

	FindByLabelID(labelID LabelUUID, offset, limit uint64) (questionIDs []QuestionUUID, nv protocol.NumberOfVersion, err protocol.Error)
	ListLabelIDs(questionID QuestionUUID, offset, limit uint64) (labelIDs []LabelUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
