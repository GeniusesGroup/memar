/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// EducationCertificateIssuer indicate the domain record data fields.
type EducationCertificateIssuer interface {
	IssuerID() protocol.UserID                   // organization only??
	KnowledgeUnitID() EducationKnowledgeUnitUUID //
	Score() uint64                               //
	Time() protocol.Time                         // save time
	RequestID() UserRequestUUID                  // user-request domain
}
