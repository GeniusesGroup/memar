/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// FinancialAccountID indicate the domain record data fields.
// It is about settlement reference internal ID like bank account ID.
type FinancialAccountID interface {
	AccountID() FinancialAccountUUID 
	ID() string                      //
	Time() protocol.Time             // save time
	RequestID() urp.UserRequestUUID  //
}

type FinancialAccountID_StorageServices interface {
	Save(dm FinancialAccountID) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(accountID FinancialAccountUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(accountID FinancialAccountUUID, vo protocol.VersionOffset) (dm FinancialAccountID, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_AccountIDs_BY_ID(id string) (accountIDs []FinancialAccountUUID, err protocol.Error)
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
