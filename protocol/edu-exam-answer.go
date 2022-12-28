/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// EducationAnswer indicate the domain record data fields.
type EducationAnswer interface {
	QuestionID() EducationQuestionUUID //
	UserID() protocol.UserID           //
	Answer() string                    // A
	Status() EducationAnswer_Status    //
	Time() protocol.Time               // save time
	RequestID() UserRequestUUID        // user-request domain
}

type EducationAnswer_Status uint8

const (
	EducationAnswer_Unset EducationAnswer_Status = iota
	EducationAnswer_Passed
	EducationAnswer_Failed
)
