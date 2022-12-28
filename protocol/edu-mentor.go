/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// EducationMentor indicate the domain record data fields.
type EducationMentor interface {
	UserID() protocol.UserID                     //
	KnowledgeUnitID() EducationKnowledgeUnitUUID //
	Type() EducationMentor_Type                  // education unit type
	Time() protocol.Time                         // save time
	RequestID() UserRequestUUID                  // user-request domain
}

type EducationMentor_Type uint8

const (
	EducationMentor_Type_Unset EducationMentor_Type = iota
	EducationMentor_Type_OrganizationStaff
	EducationMentor_Type_SelfStatement
	EducationMentor_Type_UsersVote
	EducationMentor_Type_AI
)
