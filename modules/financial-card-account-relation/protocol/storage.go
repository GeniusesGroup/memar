/* For license and copyright information please see the LEGAL file in the code repository */

package fcarp

import (
	"memar/protocol"

	fap "org/modules/financial-account/protocol"
	fcp "org/modules/financial-card/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(accountID fap.FinancialAccountUUID, cardID fcp.FinancialCardUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(accountID fap.FinancialAccountUUID, cardID fcp.FinancialCardUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_CardIDs_BY_AccountID(accountID fap.FinancialAccountUUID, offset, limit uint64) (cardIDs []fcp.FinancialCardUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_AccountIDs_BY_CardID(cardID fcp.FinancialCardUUID, offset, limit uint64) (accountIDs []fap.FinancialAccountUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
