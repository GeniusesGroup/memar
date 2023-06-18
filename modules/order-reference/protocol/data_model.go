/* For license and copyright information please see the LEGAL file in the code repository */

package orp

import (
	"libgo/protocol"

	ftp "org/modules/financial-transaction/protocol"
	op "org/modules/order/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields. each order is immutable record.
type DataModel interface {
	OrderID() op.OrderUUID                      //
	Reference() [16]byte                        // Any ID that user can assign to track for any purpose. It can't be nil.
	ReferenceType() ftp.FinancialTransaction_RT //
	SaveTime() protocol.Time                    //
	RequestID() urp.UserRequestUUID             //
}
