/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type QuestionnaireRespondentUUID protocol.UUID

// QuestionnaireRespondent indicate the domain record data fields.
type QuestionnaireRespondent interface {
	QuestionnaireRespondentID() QuestionnaireRespondentUUID //
	QuestionnaireOrderID() QuestionnaireOrderUUID           //
	AnswerBy() UserUUID                                     //
	FillBy() UserUUID                                       //
	Time() protocol.Time                                    // Save time
	RequestID() urp.UserRequestUUID                         //
}
