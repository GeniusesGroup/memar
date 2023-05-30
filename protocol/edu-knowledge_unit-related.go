/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// EducationKnowledgeUnitRelated indicate the domain record data fields.
type EducationKnowledgeUnitRelated interface {
	SuggesterID() up.UserUUID          //
	Side1() EducationKnowledgeUnitUUID //
	Priority() uint64                  //
	Level() uint64                     //
	Side2() EducationKnowledgeUnitUUID //
	Time() protocol.Time               // save time
	RequestID() urp.UserRequestUUID    //
}
