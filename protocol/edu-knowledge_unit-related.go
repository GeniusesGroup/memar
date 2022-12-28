/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// EducationKnowledgeUnitRelated indicate the domain record data fields.
type EducationKnowledgeUnitRelated interface {
	SuggesterID() protocol.UserID      //
	Side1() EducationKnowledgeUnitUUID //
	Priority() uint64                  //
	Level() uint64                     //
	Side2() EducationKnowledgeUnitUUID //
	Time() protocol.Time               // save time
	RequestID() UserRequestUUID        // user-request domain
}
