/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// TODO::: Optional module

// InviteTask indicate the domain record data fields.
type InviteTask interface {
	InviteID() InviteUUID       //
	TaskID() TaskUUID           //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}
