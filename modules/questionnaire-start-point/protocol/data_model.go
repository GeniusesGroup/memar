/* For license and copyright information please see the LEGAL file in the code repository */

package qspp

import (
	"libgo/protocol"

	qp "org/modules/questionnaire/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionnaireID() qp.QuestionnaireUUID //
	// TODO::: embed or copy??
	protocol.Time                   //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
