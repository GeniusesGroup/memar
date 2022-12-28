/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// EducationExamRelated indicate the domain record data fields.
type EducationExamRelated interface {
	SuggesterID() protocol.UserID //
	Side1() EducationExamUUID     //
	Priority() uint64             //
	Level() uint64                //
	Side2() EducationExamUUID     //
	Time() protocol.Time          // save time
	RequestID() UserRequestUUID   // user-request domain
}
