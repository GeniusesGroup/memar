/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// EduCertificate indicate the domain record data fields.
type EduCertificate interface {
	CertificateID() [16]byte                     //
	KnowledgeUnitID() EducationKnowledgeUnitUUID //
	IssuedByID() UserUUID                        // organization only??
	IssuedForID() UserUUID                       //
	Score() uint64                               //
	IssueTime() protocol.Time                    //
	Time() protocol.Time                         // save time
	RequestID() urp.UserRequestUUID              //
}
