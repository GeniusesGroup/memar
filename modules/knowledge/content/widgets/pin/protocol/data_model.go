/* For license and copyright information please see the LEGAL file in the code repository */

package cp_p

import (
	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"

	comment_p "org/modules/knowledge/content/edges-loop/comment/protocol"
	group_p "org/modules/management/group/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	comment_p.Field_CommentID
	group_p.Field_GroupID
	CommentPinedID() comment_p.UUID

	request_p.Field_RequestID
	audit_time_p.Field_Request
}

// Unpin service : Hidden status to unpin a comment
