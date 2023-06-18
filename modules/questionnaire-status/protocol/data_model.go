/* For license and copyright information please see the LEGAL file in the code repository */

package qsp

import (
	"libgo/protocol"

	qp "org/modules/questionnaire/protocol"
	qsp "org/modules/quiddity-status/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionnaireID() qp.QuestionnaireUUID //
	Status() Status                        //
	SaveTime() protocol.Time               // Save time
	RequestID() urp.UserRequestUUID        //
}

type Status qsp.Quiddity_Status

const (
	Status_Terminated = Status(qsp.Quiddity_Status_FreeFlag << iota) // Wait to approve
)
