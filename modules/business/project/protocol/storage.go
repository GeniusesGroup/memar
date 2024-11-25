/* For license and copyright information please see the LEGAL file in the code repository */

package project_p

import (
	error_p "memar/error/protocol"

	user_p "org/modules/identity/user/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (err error_p.Error)

	Get(projectID UUID, vo storage_p.VersionOffset) (dm DataModel, err error_p.Error)

	FIND_UserIDs_By_ProjectID(projectID UUID, offset, limit uint64) (userIDs []user_p.UUID, err error_p.Error)
}
