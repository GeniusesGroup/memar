/* For license and copyright information please see the LEGAL file in the code repository */

package exqsp

import (
	"libgo/protocol"

	eeqp "org/modules/edu-exam-question/protocol"
	qsp "org/modules/quiddity-status/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionID() eeqp.EducationQuestionUUID // don't point to quiddity title na don't set title
	Status() Status                         //
	SaveTime() protocol.Time                //
	RequestID() urp.UserRequestUUID         //
}

type Status qsp.Quiddity_Status

const (
	Status_Deprecate = Status(qsp.Quiddity_Status_FreeFlag << iota)
)
