/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// PosProvider or pos operator is to supply a particular service.
type PosCash interface {
	PosID() [16]byte                    // pos domain
	AccountID() [16]byte                // financial-account domain
	MaxCash() protocol.MoneyAmount      //
	MaxCashTransfer() protocol.Duration // from reach the max limit
	Time() protocol.Time                // save time
	RequestID() UserRequestUUID         // user-request domain
}
