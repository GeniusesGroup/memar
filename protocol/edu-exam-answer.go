/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// EducationAnswer indicate the domain record data fields.
type EducationAnswer interface {
	QuestionID() EducationQuestionUUID //
	UserID() up.UserUUID               //
	Answer() string                    // A
	Status() EducationAnswer_Status    //
	Time() protocol.Time               // save time
	RequestID() urp.UserRequestUUID    //
}

type EducationAnswer_Status uint8

const (
	EducationAnswer_Unset EducationAnswer_Status = iota
	EducationAnswer_Passed
	EducationAnswer_Failed
)
