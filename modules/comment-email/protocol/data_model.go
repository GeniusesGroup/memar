/* For license and copyright information please see the LEGAL file in the code repository */

package cep

import (
	"memar/protocol"

	cp "org/modules/comment/protocol"
)

// DataModel indicate the domain record data fields.
// TODO::: email subject force to make new comment and save all emails as reply to it in that subject.
type DataModel interface {
	CommentID() cp.CommentUUID //
	From() string              // name<username@domain>
	To() string                // name<username@domain>
	CC() string                // name<username@domain>; name<username@domain>
	BCC() string               // name<username@domain>
	Subject() string           //
	Senders() []string         // domain

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
