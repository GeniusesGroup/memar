/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

type OrgShareholder interface {
	UserID() protocol.UserID        // user domain
	Quantity() protocol.PerTrillion //
	Time() protocol.Time            // save time
	RequestID() UserRequestUUID     // user-request domain
}
