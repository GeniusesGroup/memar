/* For license and copyright information please see the LEGAL file in the code repository */

package gsp

import (
	"libgo/protocol"

	csep "org/modules/comment-settings/protocol"
	cssp "org/modules/comment-status/protocol"
	gp "org/modules/group/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	GroupID() gp.GroupUUID //
	// ArchiveThreadAfter() protocol.Duration //
	BlockedWords() []string         //
	DefaultSettings() csep.Settings //
	DefaultStatus() cssp.Status     //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
