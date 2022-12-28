/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// OrderReference indicate the domain record data fields. each order is immutable record.
type OrderReference interface {
	OrderID() OrderUUID                     //
	Reference() [16]byte                    // Any ID that user can assign to track for any purpose. It can't be nil.
	ReferenceType() FinancialTransaction_RT //
	Time() protocol.Time                    // save time
	RequestID() UserRequestUUID             // user-request domain
}
