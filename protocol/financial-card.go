/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/iso"
	"libgo/protocol"
	urp "org/modules/user-request/protocol"
)

type FinancialCardUUID = protocol.UUID

// FinancialCard indicate the domain record data fields.
type FinancialCard interface {
	FinancialCardID() FinancialCardUUID //
	Issuer() UserUUID                   //, any org user
	UserID() UserUUID                   //, owner of the card
	CardNumber() iso.Card               //
	ExpireDate() protocol.Time          //
	CVC() uint16                        //
	Time() protocol.Time                // save time
	RequestID() urp.UserRequestUUID     //
}

type FinancialCard_StorageServices interface {
	Save(fc FinancialCard) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(financialCardID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(financialCardID [16]byte, vo protocol.VersionOffset) (fc FinancialCard, nv protocol.NumberOfVersion, err protocol.Error)

	FindByUser(userID UserUUID, offset, limit uint64) (financialCardIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
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
