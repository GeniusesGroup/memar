/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// FinancialCardAccountRelation indicate the domain record data fields.
type FinancialCardAccountRelation interface {
	CardID() FinancialCardUUID                   // financial-card domain
	AccountID() FinancialAccountUUID             // financial-account domain
	Priority() uint64                            //
	Status() FinancialCardAccountRelation_Status //
	Time() protocol.Time                         // save time
	RequestID() urp.UserRequestUUID              //
}

type FinancialCardAccountRelation_StorageServices interface {
	Save(dm FinancialCardAccountRelation) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(accountID FinancialAccountUUID, cardID FinancialCardUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(accountID FinancialAccountUUID, cardID FinancialCardUUID, vo protocol.VersionOffset) (dm FinancialCardAccountRelation, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_CardIDs_BY_AccountID(accountID FinancialAccountUUID, offset, limit uint64) (cardIDs []FinancialCardUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_AccountIDs_BY_CardID(cardID FinancialCardUUID, offset, limit uint64) (accountIDs []FinancialAccountUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

type FinancialCardAccountRelation_Status Quiddity_Status

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
