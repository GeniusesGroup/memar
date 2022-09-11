/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// PosFinancialAccount or pos operator is to supply a particular service.
type PosFinancialAccount interface {
	PosID() [16]byte            // pos domain
	AccountID() [16]byte        // financial-account domain
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}
