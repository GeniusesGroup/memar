/* For license and copyright information please see the LEGAL file in the code repository */

package qarp

import (
	"libgo/protocol"

	qap "org/modules/question_answer/protocol"
	urp "org/modules/user-request/protocol"
	
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	AnswerID() qap.AnswerUUID       //
	Answer() uint8                  //
	SaveTime() protocol.Time        // Save time
	RequestID() urp.UserRequestUUID //
}

