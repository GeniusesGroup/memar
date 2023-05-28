/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// QuestionnaireStatus indicate the domain record data fields.
type QuestionnaireStatus interface {
	QuestionnaireID() QuestionnaireUUID //
	Status() Questionnaire_Status       //
	Time() protocol.Time                // Save time
	RequestID() urp.UserRequestUUID     //
}

type Questionnaire_Status Quiddity_Status

const (
	Questionnaire_Status_Terminated = Questionnaire_Status(Quiddity_Status_FreeFlag << iota) // Wait to approve
)
