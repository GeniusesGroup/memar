/* For license and copyright information please see the LEGAL file in the code repository */

package fcsp

import (
	"memar/protocol"

	fcp "org/modules/financial-card/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(cardID fcp.FinancialCardUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(cardID fcp.FinancialCardUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FindByCardHexSHA1(cardHexSHA1 CardHexSHA1, offset, limit uint64) (cardIDs []fcp.FinancialCardUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
