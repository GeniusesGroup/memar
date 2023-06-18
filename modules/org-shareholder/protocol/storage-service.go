/* For license and copyright information please see the LEGAL file in the code repository */

package osp

import (
	"libgo/protocol"

	org "org/modules/org/protocol"
	up "org/modules/user/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(orgID org.OrgUUID, userID up.UserUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(orgID org.OrgUUID, userID up.UserUUID, vo protocol.VersionOffset) (dm DataModel, err protocol.Error)

	LIST_UserIDs_BY_OrgID(orgID org.OrgUUID, offset, limit uint64) (userIDs []up.UserUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
