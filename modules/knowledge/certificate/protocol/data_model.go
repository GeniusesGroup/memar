/* For license and copyright information please see the LEGAL file in the code repository */

package ecp

import (
	time_p "memar/time/protocol"

	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"

	user_p "org/modules/identity/user/protocol"
	eku_p "org/modules/knowledge/knowledge_unit/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	Field_CertificateID
	eku_p.Field_KnowledgeUnitID
	IssuedByID() user_p.UUID // organization only??
	IssuedForID() user_p.UUID
	Score() uint64
	IssueTime() time_p.Time

	request_p.Field_RequestID
	audit_time_p.Field_Request
}
