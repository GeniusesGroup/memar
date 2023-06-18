/* For license and copyright information please see the LEGAL file in the code repository */

package rrrp

import (
	"libgo/protocol"

	rp "org/modules/role/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	RoleID() rp.RoleUUID            //
	OtherID() rp.RoleUUID           //
	Type() Type                     //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Type uint8

const (
	Type_Unset Type = iota
	Type_SameLevel
	Type_UpperLevel
	Type_LowerLevel
)
