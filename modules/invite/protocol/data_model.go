/* For license and copyright information please see the LEGAL file in the code repository */

package ip

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	InviteID() InviteUUID           //
	Type() Type                     //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Type uint32

const (
	Type_Unset Type = 0
	Type_      Type = (1 << iota)
	Type_WaitList
)

// TODO::: user send last time of active state record plus its ID and optional invited user id as invite code.
