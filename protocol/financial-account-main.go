/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// FinancialAccountMain indicate the domain record data fields.
type FinancialAccountMain interface {
	UserID() UserUUID               //
	Currency() [16]byte             // financial-currency
	AccountID() [16]byte            // financial-account domain
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type FinancialAccountMain_StorageServices interface {
	Save(fa FinancialAccountMain) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(userID, currency [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(userID, currency [16]byte, vo protocol.VersionOffset) (fa FinancialAccountMain, nv protocol.NumberOfVersion, err protocol.Error)
}
