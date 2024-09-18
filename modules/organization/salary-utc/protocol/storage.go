/* For license and copyright information please see the LEGAL file in the code repository */

package osup

import (
	"memar/protocol"

	fcp "org/modules/financial-currency/protocol"
	org "org/modules/org/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(orgID org.OrgUUID, currencyID fcp.FinancialCurrencyUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(orgID org.OrgUUID, currencyID fcp.FinancialCurrencyUUID, vo protocol.VersionOffset) (dm DataModel, err protocol.Error)
}
