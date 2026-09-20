/* For license and copyright information please see the LEGAL file in the code repository */

package fcdp

import (
	error_p "memar/process/error/protocol"

	storage_p "memar/storage/protocol"
	user_p "org/modules/identity/user/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv storage_p.NumberOfVersion, err error_p.Error)

	Count(userID user_p.UUID) (nv storage_p.NumberOfVersion, err error_p.Error)
	Get(userID user_p.UUID, vo storage_p.VersionOffset) (dm DataModel, nv storage_p.NumberOfVersion, err error_p.Error)
}
