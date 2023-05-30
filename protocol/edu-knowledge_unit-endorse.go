/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// EducationKnowledgeUnitEndorse indicate the domain record data fields.
type EducationKnowledgeUnitEndorse interface {
	UserID() UserUUID                            //
	KnowledgeUnitID() EducationKnowledgeUnitUUID //
	EndorserID() UserUUID                        //
	Score() uint64                               //
	Time() protocol.Time                         // save time
	RequestID() urp.UserRequestUUID              //
}
