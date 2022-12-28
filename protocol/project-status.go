/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// Project indicate the domain record data fields.
type ProjectStatus interface {
	ProjectID() ProjectUUID     // group domain. use to get and show locale title.
	Status() Project_Status     //
	Time() protocol.Time        // Save time
	RequestID() UserRequestUUID // user-request domain
}

type Project_Status Quiddity_Status
