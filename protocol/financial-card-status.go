/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// FinancialCardStatus indicate the domain record data fields.
type FinancialCardStatus interface {
	FinancialCardID() FinancialCardUUID //
	Status()                            //
	Time() protocol.Time                // save time
	RequestID() urp.UserRequestUUID     //
}

type FinancialCardStatus_StorageServices interface {
	Save(fcs FinancialCardStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(financialCardID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(financialCardID [16]byte, vo protocol.VersionOffset) (fcs FinancialCardStatus, nv protocol.NumberOfVersion, err protocol.Error)
}
