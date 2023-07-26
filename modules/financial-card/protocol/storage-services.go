/* For license and copyright information please see the LEGAL file in the code repository */

package fcp

import (
	"memar/iso"
	"memar/protocol"
	up "org/modules/user/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(financialCardID FinancialCardUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(financialCardID FinancialCardUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_FinancialCardIDs_BY_UserID(userID up.UserUUID, offset, limit uint64) (financialCardIDs []FinancialCardUUID, nv protocol.NumberOfVersion, err protocol.Error)
	FIND_FinancialCardIDs_BY_CardNumber(cardNumber iso.Card) (financialCardIDs []FinancialCardUUID, err protocol.Error)
}
