/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

type LabelUUID = protocol.UUID

// Label indicate the domain record data fields.
type Label interface {
	LabelID() LabelUUID         //
	Time() protocol.Time        // Save time
	RequestID() UserRequestUUID // user-request domain
}
