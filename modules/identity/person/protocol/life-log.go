/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// LifeLog indicate the domain record data fields.
type LifeLog interface {
	UserID() [16]byte           // user-status domain
	Type() LifeLog_Type         //
	Start() protocol.Time       //
	End() protocol.Time         //
	Time() protocol.Time        // Save time
	RequestID() UserRequestUUID // user-request domain
}

type LifeLog_Type uint8
