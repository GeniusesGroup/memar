/* For license and copyright information please see the LEGAL file in the code repository */

package dcpp

import (
	"memar/protocol"

	fcp "org/modules/financial-card/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(financialCardID fcp.FinancialCardUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(financialCardID fcp.FinancialCardUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)
}
