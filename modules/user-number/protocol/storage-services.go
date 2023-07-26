/* For license and copyright information please see the LEGAL file in the code repository */

package unp

import (
	"memar/protocol"

	org "org/modules/org/protocol"
	up "org/modules/user/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(userID up.UserUUID, orgID org.OrgUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(userID up.UserUUID, orgID org.OrgUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FindByNumber(number uint64, offset, limit uint64) (userIDs []up.UserUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
