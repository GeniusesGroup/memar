/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/iso"
	"github.com/GeniusesGroup/libgo/protocol"
)

type FinancialCardUUID = protocol.UUID

// FinancialCard indicate the domain record data fields.
type FinancialCard interface {
	FinancialCardID() FinancialCardUUID //
	Issuer() protocol.UserID            // user domain, any org user
	UserID() protocol.UserID            // user domain, owner of the card
	CardNumber() iso.Card               //
	ExpireDate() protocol.Time          //
	CVC() uint16                        //
	Time() protocol.Time                // save time
	RequestID() UserRequestUUID         // user-request domain
}

type FinancialCard_StorageServices interface {
	Save(fc FinancialCard) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(financialCardID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(financialCardID [16]byte, vo protocol.VersionOffset) (fc FinancialCard, nv protocol.NumberOfVersion, err protocol.Error)

	FindByUser(userID [16]byte, offset, limit uint64) (financialCardIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
	FindByCardNumber(cardNumber iso.Card) (financialCardID [16]byte, err protocol.Error)
}

type FinancialCard_Service_Register_Request interface {
	AccountID() [16]byte
	CardNumber() iso.Card
	ExpireDate() protocol.Time
	CVC() uint16
}

type FinancialCard_Service_Get_Request interface {
	AccountID() [16]byte
	VersionOffset() protocol.VersionOffset
}
type FinancialCard_Service_Get_Response interface {
	FinancialCard
	Numbers() uint64
}
