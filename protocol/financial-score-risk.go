/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// FinancialRiskScore
// Store user risk to prevent or detect frauds
type FinancialRiskScore interface {
	UserID() UserUUID               //
	Score() int64                   //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}
