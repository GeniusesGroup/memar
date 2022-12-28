/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

type ContractAnalytic interface {
	CoordinateID() [16]byte // contract domain

	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}
