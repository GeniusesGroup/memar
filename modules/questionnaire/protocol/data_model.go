/* For license and copyright information please see the LEGAL file in the code repository */

package qp

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionnaireID() QuestionnaireUUID //
	Type() Type                         //
	SaveTime() protocol.Time            //
	RequestID() urp.UserRequestUUID     //
}

type Type uint16

const (
	Type_Unset Type = 0
	Type_Quiz  Type = (1 << iota)
	Type_Anonymous
	Type_Duration
	Type_StartPoint
	Type_AllowToEdit
	Type_Form
	Type_MaxAttempt

	// No one can made direct answer to this questionnaire.
	Type_Criterion

	// TODO::: Template for forms?
)

// link to group
