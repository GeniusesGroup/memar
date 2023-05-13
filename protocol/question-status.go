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
	RequestID() urp.UserRequestUUID // user-request domain
}

type Question_Status Quiddity_Status

const (
	Question_Status_Terminated = Question_Status(Quiddity_Status_FreeFlag << iota) // Wait to approve
)
