/* For license and copyright information please see the LEGAL file in the code repository */

package faip

import (
	"libgo/iso"
	"libgo/protocol"

	fap "org/modules/financial-account/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	AccountID() fap.FinancialAccountUUID // financial-account domain
	IBAN() iso.IBAN                      //
	SaveTime() protocol.Time             //
	RequestID() urp.UserRequestUUID      //
}
