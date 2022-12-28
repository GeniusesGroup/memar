/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// FinancialCardPin indicate the domain record data fields.
type FinancialCardPin interface {
	FinancialCardID() FinancialCardUUID //
	FixedPin1() uint32                  //
	FixedPin2() uint32                  //
	DynamicPin1() []byte                // OTP key
	DynamicPin2() []byte                // OTP key
	Time() protocol.Time                // save time
	RequestID() UserRequestUUID         // user-request domain
}

type FinancialCardPin_StorageServices interface {
	Save(fac FinancialCardPin) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(financialCardID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(financialCardID [16]byte, vo protocol.VersionOffset) (fac FinancialCardPin, nv protocol.NumberOfVersion, err protocol.Error)
}
