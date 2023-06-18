/* For license and copyright information please see the LEGAL file in the code repository */

package emp

import (
	"libgo/protocol"

	ekup "org/modules/edu-knowledge_unit/protocol"
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	UserID() up.UserUUID                              //
	KnowledgeUnitID() ekup.EducationKnowledgeUnitUUID //
	Type() Type                                       // education unit type
	SaveTime() protocol.Time                          //
	RequestID() urp.UserRequestUUID                   //
}

type Type uint8

const (
	Type_Unset Type = iota
	Type_OrganizationStaff
	Type_SelfStatement
	Type_UsersVote
	Type_AI
)
