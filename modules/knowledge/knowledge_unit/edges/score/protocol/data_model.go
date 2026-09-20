/* For license and copyright information please see the LEGAL file in the code repository */

package kus_p

import (
	"memar/time/duration"

	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"

	user_p "org/modules/identity/user/protocol"
	ku_p "org/modules/knowledge/knowledge_unit/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	user_p.Field_UserUUID
	ku_p.Field_KnowledgeUnitID
	GivenScoreID() user_p.UUID
	LearnDuration() duration.Second
	Score() uint64

	request_p.Field_RequestID
	audit_time_p.Field_Request
}
