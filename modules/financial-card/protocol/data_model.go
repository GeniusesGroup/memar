/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/iso"
	"libgo/protocol"
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

type FinancialCardUUID = protocol.UUID

// FinancialCard indicate the domain record data fields.
type FinancialCard interface {
	FinancialCardID() FinancialCardUUID //
	Issuer() up.UserUUID                //, any org user
	UserID() up.UserUUID                //, owner of the card
	CardNumber() iso.Card               //
	ExpireDate() protocol.Time          //
	CVC() uint16                        //
	Time() protocol.Time                // save time
	RequestID() urp.UserRequestUUID     //
}

type FinancialCard_StorageServices interface {
	Save(f FinancialCard) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(financialCardID FinancialCardUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(financialCardID FinancialCardUUID, vo protocol.VersionOffset) (f FinancialCard, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_FinancialCardIDs_BY_UserID(userID up.UserUUID, offset, limit uint64) (financialCardIDs []FinancialCardUUID, nv protocol.NumberOfVersion, err protocol.Error)
	FIND_FinancialCardIDs_BY_CardNumber(cardNumber iso.Card) (financialCardIDs []FinancialCardUUID, err protocol.Error)
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
