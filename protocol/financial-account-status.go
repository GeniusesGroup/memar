/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// FinancialAccountStatus indicate the domain record data fields.
type FinancialAccountStatus interface {
	AccountID() [16]byte             // financial-account domain
	Status() FinancialAccount_Status //
	Time() protocol.Time             // save time
	RequestID() UserRequestUUID      // user-request domain
}

type FinancialAccountStatus_StorageServices interface {
	Save(fas FinancialAccountStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(accountID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(accountID [16]byte, vo protocol.VersionOffset) (fas FinancialAccountStatus, nv protocol.NumberOfVersion, err protocol.Error)

	FilterByStatus(status FinancialAccount_Status, offset, limit uint64) (accountIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}

type FinancialAccount_Status Quiddity_Status

const (
	FinancialAccount_Status_Closed = FinancialAccount_Status(Quiddity_Status_FreeFlag << iota)
)
