/* For license and copyright information please see the LEGAL file in the code repository */

package thp

import (
	"memar/protocol"

	cp "org/modules/comment/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
// home timeline feed
type DataModel interface {
	UserID() up.UserUUID
	CommentID() cp.CommentUUID
	ReasonUserID() up.UserUUID // it can be the owner of comment or any other user base on reason
	Reason() Reason
	// TODO::: node details??

	// protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
