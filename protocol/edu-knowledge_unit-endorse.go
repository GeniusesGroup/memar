/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// EducationKnowledgeUnitEndorse indicate the domain record data fields.
type EducationKnowledgeUnitEndorse interface {
	UserID() protocol.UserID                     //
	KnowledgeUnitID() EducationKnowledgeUnitUUID //
	EndorserID() protocol.UserID                 //
	Score() uint64                               //
	Time() protocol.Time                         // save time
	RequestID() UserRequestUUID                  // user-request domain
}
