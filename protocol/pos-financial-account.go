/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// PosFinancialAccount or pos operator is to supply a particular service.
type PosFinancialAccount interface {
	PosID() PosUUID                  //
	AccountID() FinancialAccountUUID //
	Status() PosFinancialAccount_Status
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type PosFinancialAccount_StorageServices interface {
	Save(dm PosFinancialAccount) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(posID PosUUID, accountID FinancialAccountUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(posID PosUUID, accountID FinancialAccountUUID, vo protocol.VersionOffset) (dm PosFinancialAccount, err protocol.Error)

	LIST_AccountIDs_BY_PosIDs(posID PosUUID, offset, limit uint64) (accountIDs []FinancialAccountUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_PosIDs_BY_AccountID(AccountID FinancialAccountUUID, offset, limit uint64) (posIDs []PosUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

type PosFinancialAccount_Status Quiddity_Status
