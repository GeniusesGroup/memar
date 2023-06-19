/* For license and copyright information please see the LEGAL file in the code repository */

package qrlp

import (
	"libgo/protocol"

	lp "org/modules/label/protocol"
	qp "org/modules/questionnaire/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionnaireID() qp.QuestionnaireUUID //
	Label() lp.LabelUUID                   //
	SaveTime() protocol.Time               //
	RequestID() urp.UserRequestUUID        //
}
