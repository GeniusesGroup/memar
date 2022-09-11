/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// InviteDelegate indicate the domain record data fields.
type InviteDelegate interface {
	InviteID() InviteUUID //
	InviteDelegate_Type() InviteDelegate_Type
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type InviteDelegate_Type uint32

const (
	InviteDelegate_Type_Unset  InviteDelegate_Type = 0
	InviteDelegate_Type_1st_Friend  InviteDelegate_Type = (1 << iota)
	InviteDelegate_Type_2st_Friend
	InviteDelegate_Type_3st_Friend
	InviteDelegate_Type_4st_Friend
	InviteDelegate_Type_5st_Friend
	InviteDelegate_Type_6st_Friend
	InviteDelegate_Type_Family
	// InviteDelegate_Type_
)
