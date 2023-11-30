/* For license and copyright information please see the LEGAL file in the code repository */

package cop

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	cp "org/modules/comment/protocol"
	op "org/modules/object/protocol"
)

// DataModel indicate the domain record data fields.
// Object can be any such as image, video, voice, ...
type DataModel interface {
	CommentID() cp.CommentUUID
	ObjectID() op.ObjectUUID

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
