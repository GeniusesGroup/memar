/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// QuestionStatus indicate the domain record data fields.
type QuestionStatus interface {
	QuestionID() QuestionUUID       //
	Status() Question_Status        //
	Time() protocol.Time            // Save time
	RequestID() urp.UserRequestUUID //
}

type QuestionStatus_StorageServices interface {
	Save(dm QuestionStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(questionID QuestionUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(questionID QuestionUUID, vo protocol.VersionOffset) (dm QuestionStatus, nv protocol.NumberOfVersion, err protocol.Error)

	FILTER_QuestionIDs_BY_Status(status Question_Status, offset, limit uint64) (questionIDs []QuestionUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

type Question_Status Quiddity_Status

const (
	Question_Status_Terminated = Question_Status(Quiddity_Status_FreeFlag << iota) // Wait to approve
)
