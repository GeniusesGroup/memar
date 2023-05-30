/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// EducationMentor indicate the domain record data fields.
type EducationMentor interface {
	UserID() up.UserUUID                         //
	KnowledgeUnitID() EducationKnowledgeUnitUUID //
	Type() EducationMentor_Type                  // education unit type
	Time() protocol.Time                         // save time
	RequestID() urp.UserRequestUUID              //
}

type EducationMentor_Type uint8

const (
	EducationMentor_Type_Unset EducationMentor_Type = iota
	EducationMentor_Type_OrganizationStaff
	EducationMentor_Type_SelfStatement
	EducationMentor_Type_UsersVote
	EducationMentor_Type_AI
)
