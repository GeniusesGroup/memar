/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// Individual and General score
type FinancialScore interface {
	UserID() protocol.UserID    // user domain
	Score() int64               //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}
