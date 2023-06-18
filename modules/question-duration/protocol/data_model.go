/* For license and copyright information please see the LEGAL file in the code repository */

package qdp

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	qp "org/modules/question/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionID() qp.QuestionUUID    //
	Epoch() QuestionDuration_Epoch  //
	Duration() protocol.Duration    // from Epoch()
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}


type QuestionDuration_Epoch uint8

const (
	QuestionDuration_Epoch_Unset QuestionDuration_Epoch = iota
	QuestionDuration_Epoch_IssueDate
	QuestionDuration_Epoch_StartPoint
)
