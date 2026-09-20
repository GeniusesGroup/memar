/* For license and copyright information please see the LEGAL file in the code repository */

package ecip

import (
	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"

	ku_p "org/modules/knowledge/knowledge_unit/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ku_p.Field_KnowledgeUnitID
	Score() uint64

	request_p.Field_RequestID
	audit_time_p.Field_Request
}
