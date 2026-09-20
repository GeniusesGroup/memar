/* For license and copyright information please see the LEGAL file in the code repository */

package cg_p

import (
	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"

	comment_p "org/modules/knowledge/content/edges-loop/comment/protocol"
	group_p "org/modules/management/group/protocol"
)

// DataModel indicate the domain record data fields.
// each comment is immutable record and so use version mechanism to chain comments in a group.
type DataModel interface {
	group_p.Field_GroupID
	Field_CommentIndex // TODO::: Need index or just order by time?? index need lock!
	comment_p.Field_CommentID

	request_p.Field_RequestID
	audit_time_p.Field_Request
}
