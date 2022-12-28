/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// EduCertificate indicate the domain record data fields.
type EduCertificate interface {
	CertificateID() [16]byte                     //
	KnowledgeUnitID() EducationKnowledgeUnitUUID //
	IssuedByID() protocol.UserID                 // organization only??
	IssuedForID() protocol.UserID                //
	Score() uint64                               //
	IssueTime() protocol.Time                    //
	Time() protocol.Time                         // save time
	RequestID() UserRequestUUID                  // user-request domain
}
