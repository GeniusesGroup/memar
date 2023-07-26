/* For license and copyright information please see the LEGAL file in the code repository */

package qop

import (
	"memar/protocol"

	qp "org/modules/quiddity/protocol"
	up "org/modules/user/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(quiddityID qp.QuiddityUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(quiddityID qp.QuiddityUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FindByOwnerID(userID up.UserUUID, offset, limit uint64) (quiddityIDs []qp.QuiddityUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
