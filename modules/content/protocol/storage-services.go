/* For license and copyright information please see the LEGAL file in the code repository */

package cp

import (
	"memar/protocol"

	up "org/modules/user/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(contentID ContentUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(contentID ContentUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_ContentIDs_BY_UserID(userID up.UserUUID, offset, limit uint64) (contentIDs []ContentUUID, nv protocol.NumberOfVersion, err protocol.Error)
	GetIDs(offset, limit uint64) (contentIDs []ContentUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
