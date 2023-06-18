/* For license and copyright information please see the LEGAL file in the code repository */

package lsp

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	SkillID() SkillUUID //

	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
