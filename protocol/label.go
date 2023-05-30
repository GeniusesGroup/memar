/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type LabelUUID = protocol.UUID

// Label indicate the domain record data fields.
type Label interface {
	LabelID() LabelUUID             //
	Status() Label_Status           //
	Time() protocol.Time            // Save time
	RequestID() urp.UserRequestUUID //
}

type Label_Status Quiddity_Status
