/* For license and copyright information please see the LEGAL file in the code repository */

package faip

import (
	error_p "memar/process/error/protocol"

	storage_p "memar/storage/protocol"
	account_p "org/modules/economics/account/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv storage_p.NumberOfVersion, err error_p.Error)

	Count(accountID account_p.UUID) (nv storage_p.NumberOfVersion, err error_p.Error)
	Get(accountID account_p.UUID, vo storage_p.VersionOffset) (dm DataModel, nv storage_p.NumberOfVersion, err error_p.Error)

	FIND_AccountIDs_BY_IBAN(iban IBAN) (accountID account_p.UUID, err error_p.Error)
}
