/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/iso"
	"github.com/GeniusesGroup/libgo/protocol"
)

// FinancialAccountIBAN indicate the domain record data fields.
type FinancialAccountIBAN interface {
	AccountID() [16]byte        // financial-account domain
	IBAN() iso.IBAN             //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type FinancialAccountIBAN_StorageServices interface {
	Save(fai FinancialAccountIBAN) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(accountID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(accountID [16]byte, vo protocol.VersionOffset) (fai FinancialAccountIBAN, nv protocol.NumberOfVersion, err protocol.Error)

	FindByIBAN(iban iso.IBAN) (accountID [16]byte, err protocol.Error)
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
