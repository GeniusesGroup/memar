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
	RequestID() urp.UserRequestUUID //
}

type QuestionLabelRelation_StorageServices interface {
	Save(dm QuestionLabelRelation) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(questionID QuestionUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(questionID QuestionUUID, vo protocol.VersionOffset) (dm QuestionLabelRelation, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_QuestionIDs_BY_LabelID(labelID LabelUUID, offset, limit uint64) (questionIDs []QuestionUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_LabelIDs_BY_QuestionID(questionID QuestionUUID, offset, limit uint64) (labelIDs []LabelUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
