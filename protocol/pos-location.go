/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// PosLocation indicate the domain record data fields.
type PosLocation interface {
	PosID() [16]byte              // pos domain
	BuildingLocationID() [16]byte // building-location domain
	Time() protocol.Time          // save time
	RequestID() UserRequestUUID   // user-request domain
}
