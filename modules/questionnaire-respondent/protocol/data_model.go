/* For license and copyright information please see the LEGAL file in the code repository */

package qrp

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionnaireRespondentID() QuestionnaireRespondentUUID //
	QuestionnaireOrderID() QuestionnaireOrderUUID           //
	AnswerBy() up.UserUUID                                  //
	FillBy() up.UserUUID                                    //
	SaveTime() protocol.Time                                // Save time
	RequestID() urp.UserRequestUUID                         //
}
