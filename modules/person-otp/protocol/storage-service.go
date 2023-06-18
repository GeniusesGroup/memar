/* For license and copyright information please see the LEGAL file in the code repository */

package pop

import (
	"libgo/protocol"

	up "org/modules/user/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(personID up.UserUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(personID up.UserUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)
}
