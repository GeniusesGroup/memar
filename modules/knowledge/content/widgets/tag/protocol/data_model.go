/* For license and copyright information please see the LEGAL file in the code repository */

package ctp

import (
	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"

	comment_p "org/modules/knowledge/content/edges-loop/comment/protocol"
	text_p "org/modules/knowledge/text/protocol"
)

// TODO::: It seems this domain MUST be GUI domain only.
// Need more data e.g. tag location in a comment text, ...
// Can add `a` html tag in comment register time with or without `href` attributes

// DataModel indicate the domain record data fields.
// It must just use to index hashtag words from comment-text domain
type DataModel interface {
	comment_p.Field_CommentID
	Tags() []text_p.UUID

	request_p.Field_RequestID
	audit_time_p.Field_Request
}
