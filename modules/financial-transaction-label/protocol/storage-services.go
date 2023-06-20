/* For license and copyright information please see the LEGAL file in the code repository */

package ftp

import (
	"libgo/protocol"

	fap "org/modules/financial-account/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (err protocol.Error)

	Get(accountID fap.FinancialAccountUUID, accountOffset protocol.VersionOffset) (dm DataModel, err protocol.Error)
}
