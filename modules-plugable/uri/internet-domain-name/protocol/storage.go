/* For license and copyright information please see the LEGAL file in the code repository */

package domain_p

import (
	error_p "memar/process/error/protocol"

	storage_p "memar/storage/protocol"
	user_p "org/modules/identity/user/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv storage_p.NumberOfVersion, err error_p.Error)

	Count(domain string) (nv storage_p.NumberOfVersion, err error_p.Error)
	Get(domain string, vo storage_p.VersionOffset) (dm DataModel, nv storage_p.NumberOfVersion, err error_p.Error)

	FindByUserID(userID user_p.UUID, offset, limit uint64) (domains []string, nv storage_p.NumberOfVersion, err error_p.Error)
}
