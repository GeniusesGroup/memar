/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

type ProjectUUID = protocol.UUID

// Project indicate the domain record data fields.
type Project interface {
	ProjectID() ProjectUUID     // group domain. use to get and show locale title.
	Type() Project_Type         //
	Time() protocol.Time        // Save time
	RequestID() UserRequestUUID // user-request domain
}

type Project_Type uint64
