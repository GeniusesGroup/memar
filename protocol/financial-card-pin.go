/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// FinancialCardPin indicate the domain record data fields.
type FinancialCardPin interface {
	FinancialCardID() FinancialCardUUID //
	FixedPin1() uint32                  //
	FixedPin2() uint32                  //
	DynamicPin1() []byte                // OTP key
	DynamicPin2() []byte                // OTP key
	Time() protocol.Time                // save time
	RequestID() urp.UserRequestUUID     //
}

type FinancialCardPin_StorageServices interface {
	Save(dm FinancialCardPin) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(financialCardID FinancialCardUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(financialCardID FinancialCardUUID, vo protocol.VersionOffset) (dm FinancialCardPin, nv protocol.NumberOfVersion, err protocol.Error)
}
