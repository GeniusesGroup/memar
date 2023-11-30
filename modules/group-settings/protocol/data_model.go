/* For license and copyright information please see the LEGAL file in the code repository */

package gsp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	csep "org/modules/comment-settings/protocol"
	cssp "org/modules/comment-status/protocol"
	gp "org/modules/group/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	GroupID() gp.GroupUUID
	// ArchiveThreadAfter() protocol.Duration
	BlockedWords() []string
	DefaultSettings() csep.Settings
	DefaultStatus() cssp.Status

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
