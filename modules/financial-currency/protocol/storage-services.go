/* For license and copyright information please see the LEGAL file in the code repository */

package fcp

import (
	"memar/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(currency FinancialCurrencyUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(currency FinancialCurrencyUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)
}
