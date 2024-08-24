/* For license and copyright information please see the LEGAL file in the code repository */

package faip

import (
	"memar/iso"
	"memar/protocol"

	fap "org/modules/financial-account/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(accountID fap.FinancialAccountUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(accountID fap.FinancialAccountUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_AccountIDs_BY_IBAN(iban iso.IBAN) (accountID fap.FinancialAccountUUID, err protocol.Error)
}
