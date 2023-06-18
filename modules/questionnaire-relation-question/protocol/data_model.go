/* For license and copyright information please see the LEGAL file in the code repository */

package qrqp

import (
	"libgo/protocol"

	qp "org/modules/question/protocol"
	qrp "org/modules/questionnaire/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionnaireID() qrp.QuestionnaireUUID //
	QuestionID() qp.QuestionUUID            //
	Significance_Positive() uint64          //
	Significance_Negative() uint64          //
	Type() Type                             //
	SaveTime() protocol.Time                // Save time
	RequestID() urp.UserRequestUUID         //
}

type Type uint8

// TODO::: need types?

// LIST_QuestionIDs_BY_QuestionnaireID(questionnaireID qp.QuestionnaireUUID, offset, limit uint64) (questionIDs []qp.QuestionUUID, nv protocol.NumberOfVersion, err protocol.Error)
