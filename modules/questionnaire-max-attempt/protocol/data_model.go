/* For license and copyright information please see the LEGAL file in the code repository */

package qmap

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	qp "org/modules/questionnaire/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionnaireID() qp.QuestionnaireUUID //
	MaxAttempt() uint16                    //
	SaveTime() protocol.Time               // Save time
	RequestID() urp.UserRequestUUID        //
}

