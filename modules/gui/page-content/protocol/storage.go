/* For license and copyright information please see the LEGAL file in the code repository */

package content_p

import (
	error_p "memar/process/error/protocol"

	storage_p "memar/storage/protocol"
	user_p "org/modules/identity/user/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv storage_p.NumberOfVersion, err error_p.Error)

	Count(contentID UUID) (nv storage_p.NumberOfVersion, err error_p.Error)
	Get(contentID UUID, vo storage_p.VersionOffset) (dm DataModel, nv storage_p.NumberOfVersion, err error_p.Error)

	FIND_ContentIDs_BY_UserID(userID user_p.UUID, offset, limit uint64) (contentIDs []UUID, nv storage_p.NumberOfVersion, err error_p.Error)
	GetIDs(offset, limit uint64) (contentIDs []UUID, nv storage_p.NumberOfVersion, err error_p.Error)
}
