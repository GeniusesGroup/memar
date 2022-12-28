/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// FinancialAccountID indicate the domain record data fields.
// It is about settlement reference internal ID like bank account ID.
type FinancialAccountID interface {
	AccountID() [16]byte        // financial-account domain
	ID() string                 //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type FinancialAccountID_StorageServices interface {
	Save(fai FinancialAccountID) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(accountID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(accountID [16]byte, vo protocol.VersionOffset) (fai FinancialAccountID, nv protocol.NumberOfVersion, err protocol.Error)

	FindByID(id string) (accountIDs [][16]byte, err protocol.Error)
}

type (
	FinancialAccountID_Service_Register_Request interface {
		AccountID() [16]byte
		ID() string
	}
)

type (
	FinancialAccountID_Service_Get_Request interface {
		AccountID() [16]byte
		VersionOffset() protocol.VersionOffset
	}
	FinancialAccountID_Service_Get_Response interface {
		FinancialAccountID
		Numbers() uint64
	}
)
