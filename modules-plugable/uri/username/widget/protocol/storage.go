/* For license and copyright information please see the LEGAL file in the code repository */

package un_p

import (
	error_p "memar/process/error/protocol"

	storage_p "memar/storage/protocol"
	user_p "org/modules/identity/user/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv storage_p.NumberOfVersion, err error_p.Error)

	Count(userID, orgID user_p.UUID) (nv storage_p.NumberOfVersion, err error_p.Error)
	Get(userID, orgID user_p.UUID, vo storage_p.VersionOffset) (dm DataModel, nv storage_p.NumberOfVersion, err error_p.Error)

	FindByUsername(username string, offset, limit uint64) (userIDs []user_p.UUID, nv storage_p.NumberOfVersion, err error_p.Error)

	ListOrgs(userID user_p.UUID, offset, limit uint64) (orgIDs []user_p.UUID, nv storage_p.NumberOfVersion, err error_p.Error)
}
