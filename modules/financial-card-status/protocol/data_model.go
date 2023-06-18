/* For license and copyright information please see the LEGAL file in the code repository */

package fcsp

import (
	"libgo/protocol"

	fcp "org/modules/financial-card/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	FinancialCardID() fcp.FinancialCardUUID //
	Status()                                //
	SaveTime() protocol.Time                //
	RequestID() urp.UserRequestUUID         //
}
