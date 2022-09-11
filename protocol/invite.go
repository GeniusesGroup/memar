/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

type InviteUUID = protocol.UUID

// Invite indicate the domain record data fields.
type Invite interface {
	InviteID() InviteUUID       //
	Type() Invite_Type          //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type Invite_Type uint32

const (
	Invite_Type_Unset Invite_Type = 0
	Invite_Type_      Invite_Type = (1 << iota)
	Invite_Type_WaitList
)

// TODO::: user send last time of active state record plus its ID and optional invited user id as invite code.
