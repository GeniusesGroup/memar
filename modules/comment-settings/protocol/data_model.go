/* For license and copyright information please see the LEGAL file in the code repository */

package csp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	cp "org/modules/comment/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	CommentID() cp.CommentUUID
	Settings() Settings

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
