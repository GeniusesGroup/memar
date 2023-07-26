/* For license and copyright information please see the LEGAL file in the code repository */

package lvp

import (
	"memar/protocol"

	lp "org/modules/law/protocol"
	up "org/modules/user/protocol"
)

type StorageServices interface {
	Save(sm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(lawID lp.LawUUID, userID up.UserUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(lawID lp.LawUUID, userID up.UserUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	ListUsers(lawID lp.LawUUID, offset, limit uint64) (userIDs []up.UserUUID, nv protocol.NumberOfVersion, err protocol.Error)
	ListLaws(userID up.UserUUID, offset, limit uint64) (lawIDs []lp.LawUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
