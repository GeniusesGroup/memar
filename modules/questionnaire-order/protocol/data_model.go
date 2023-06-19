/* For license and copyright information please see the LEGAL file in the code repository */

package qop

import (
	"libgo/protocol"

	qp "org/modules/question/protocol"
	qrp "org/modules/questionnaire/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionnaireOrderID() QuestionnaireOrderUUID //
	QuestionnaireID() qrp.QuestionnaireUUID       //
	Questions() []qp.QuestionUUID                 //
	SaveTime() protocol.Time                      //
	RequestID() urp.UserRequestUUID               //
}
