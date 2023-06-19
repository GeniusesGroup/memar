/* For license and copyright information please see the LEGAL file in the code repository */

package qrrp

import (
	"libgo/protocol"

	qp "org/modules/question/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionID() qp.QuestionUUID    //
	RelationIDs() [][16]byte        // Question, Questionnaire
	RelationTypes() []Type          //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Type uint16

const (
	Type_Question Type = iota
	Type_Questionnaire
)
