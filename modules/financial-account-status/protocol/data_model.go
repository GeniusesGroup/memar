/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// FinancialAccountStatus indicate the domain record data fields.
type FinancialAccountStatus interface {
	AccountID() FinancialAccountUUID 
	Status() FinancialAccount_Status //
	Time() protocol.Time             // save time
	RequestID() urp.UserRequestUUID  //
}

type FinancialAccountStatus_StorageServices interface {
	Save(fas FinancialAccountStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(accountID FinancialAccountUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(accountID FinancialAccountUUID, vo protocol.VersionOffset) (fas FinancialAccountStatus, nv protocol.NumberOfVersion, err protocol.Error)

	FILTER_AccountIDs_BY_Status(status FinancialAccount_Status, offset, limit uint64) (accountIDs []FinancialAccountUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

type FinancialAccount_Status Quiddity_Status

const (
	FinancialAccount_Status_Closed = FinancialAccount_Status(Quiddity_Status_FreeFlag << iota)
)
