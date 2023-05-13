/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type ProjectUUID = protocol.UUID

// Project indicate the domain record data fields.
type Project interface {
	ProjectID() ProjectUUID         // group domain. use to get and show locale title.
	UserID() protocol.UserID        //
	Time() protocol.Time            // Save time
	RequestID() urp.UserRequestUUID // user-request domain
}
