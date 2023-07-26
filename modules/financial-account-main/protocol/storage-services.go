/* For license and copyright information please see the LEGAL file in the code repository */

package famp

import (
	"memar/protocol"

	fcp "org/modules/financial-currency/protocol"
	up "org/modules/user/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(userID up.UserUUID, currency fcp.FinancialCurrencyUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(userID up.UserUUID, currency fcp.FinancialCurrencyUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)
}
