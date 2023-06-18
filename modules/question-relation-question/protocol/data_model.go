/* For license and copyright information please see the LEGAL file in the code repository */

package qrqp

import (
	"libgo/protocol"

	qp "org/modules/question/protocol"
	qsp "org/modules/quiddity-status/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionID() qp.QuestionUUID    //
	RelationID() qp.QuestionUUID    //
	Type() Type                     //
	Status() Status                 //
	SaveTime() protocol.Time        // Save time
	RequestID() urp.UserRequestUUID //
}

type Type uint8

const (
	Type_Unset Type = iota
	Type_SubQuestion
	Type_Translated
	Type_Complement
	Type_Hint // use for options not descriptive type.
)

type Status qsp.Quiddity_Status
