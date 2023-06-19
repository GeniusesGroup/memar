/* For license and copyright information please see the LEGAL file in the code repository */

package qop

import (
	"libgo/protocol"

	qp "org/modules/question/protocol"
	qop "org/modules/question_option/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionID() qp.QuestionUUID       //
	Options() []qop.QuestionOptionUUID //
	Type() Type                        //
	AlgorithmType() AlgorithmType      //
	SaveTime() protocol.Time           //
	RequestID() urp.UserRequestUUID    //
}

type AlgorithmType uint8

const (
	AlgorithmType_Unset AlgorithmType = iota
	AlgorithmType_UserID
	AlgorithmType_StaffID
	AlgorithmType_RegisteredTime
)

type Type uint16

const (
	Type_Unset    Type = 0
	Type_DropList Type = (1 << iota)
)
