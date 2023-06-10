/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/iso"
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// FinancialAccountIBAN indicate the domain record data fields.
type FinancialAccountIBAN interface {
	AccountID() FinancialAccountUUID // financial-account domain
	IBAN() iso.IBAN                  //
	Time() protocol.Time             // save time
	RequestID() urp.UserRequestUUID  //
}

type FinancialAccountIBAN_StorageServices interface {
	Save(dm FinancialAccountIBAN) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(accountID FinancialAccountUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(accountID FinancialAccountUUID, vo protocol.VersionOffset) (dm FinancialAccountIBAN, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_AccountIDs_BY_IBAN(iban iso.IBAN) (accountID FinancialAccountUUID, err protocol.Error)
}

type FinancialAccountIBAN_Service_Register_Request interface {
	AccountID() [16]byte
	IBAN() iso.IBAN
}

type FinancialAccountIBAN_Service_Get_Request interface {
	AccountID() [16]byte
	VersionOffset() protocol.VersionOffset
}
type FinancialAccountIBAN_Service_Get_Response interface {
	FinancialAccountIBAN
	Numbers() uint64
}
