/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// FinancialCardAccountRelation indicate the domain record data fields.
type FinancialCardAccountRelation interface {
	CardID() FinancialCardUUID                   // financial-card domain
	AccountID() FinancialAccountUUID             // financial-account domain
	Priority() uint64                            //
	Status() FinancialCardAccountRelation_Status //
	Time() protocol.Time                         // save time
	RequestID() UserRequestUUID                  // user-request domain
}

type FinancialCardAccountRelation_StorageServices interface {
	Save(f FinancialCardAccountRelation) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(accountID, cardID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(accountID, cardID [16]byte, vo protocol.VersionOffset) (f FinancialCardAccountRelation, nv protocol.NumberOfVersion, err protocol.Error)

	ListCard(accountID [16]byte, offset, limit uint64) (cardIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
	ListAccount(cardID [16]byte, offset, limit uint64) (accountIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}

type FinancialCardAccountRelation_Status = Quiddity_Status

const (
// FinancialCardAccountRelation_Status_ = FinancialCardAccountRelation_Status(Quiddity_Status_FreeFlag << iota)
)

type (
	FinancialCardAccountRelation_Service_Register_Request interface {
		AccountID() [16]byte
		FinancialCardID() [16]byte
		Priority() uint64
		Status() FinancialCardAccountRelation_Status
	}
)

type (
	FinancialCardAccountRelation_Service_Get_Request interface {
		AccountID() [16]byte
		FinancialCardID() [16]byte
		VersionOffset() protocol.VersionOffset
	}
	FinancialCardAccountRelation_Service_Get_Response1 = FinancialCardAccountRelation
	FinancialCardAccountRelation_Service_Get_Response2 = protocol.VersionOffset
)
