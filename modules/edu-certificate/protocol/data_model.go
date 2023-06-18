/* For license and copyright information please see the LEGAL file in the code repository */

package ecp

import (
	"libgo/protocol"

	ekup "org/modules/edu-knowledge_unit/protocol"
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	CertificateID() [16]byte                          //
	KnowledgeUnitID() ekup.EducationKnowledgeUnitUUID //
	IssuedByID() up.UserUUID                          // organization only??
	IssuedForID() up.UserUUID                         //
	Score() uint64                                    //
	IssueTime() protocol.Time                         //
	SaveTime() protocol.Time                          //
	RequestID() urp.UserRequestUUID                   //
}
