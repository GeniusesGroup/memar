/* For license and copyright information please see the LEGAL file in the code repository */

package dcpp

import (
	"libgo/protocol"

	fcp "org/modules/financial-card/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	FinancialCardID() fcp.FinancialCardUUID //
	FixedPin1() uint32                      //
	FixedPin2() uint32                      //
	DynamicPin1() []byte                    // OTP key
	DynamicPin2() []byte                    // OTP key
	SaveTime() protocol.Time                //
	RequestID() urp.UserRequestUUID         //
}
