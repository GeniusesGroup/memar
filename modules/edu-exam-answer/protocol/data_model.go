/* For license and copyright information please see the LEGAL file in the code repository */

package exap

import (
	"libgo/protocol"

	eeqp "org/modules/edu-exam-question/protocol"
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionID() eeqp.EducationQuestionUUID //
	UserID() up.UserUUID                    //
	Answer() string                         // A
	Status() Status                         //
	SaveTime() protocol.Time                //
	RequestID() urp.UserRequestUUID         //
}

type Status uint8

const (
	EducationAnswer_Unset Status = iota
	EducationAnswer_Passed
	EducationAnswer_Failed
)
