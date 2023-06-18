/* For license and copyright information please see the LEGAL file in the code repository */

package udp

import (
	"libgo/protocol"

	up "org/modules/user/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(domain string) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(domain string, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FindByUserID(userID up.UserUUID, offset, limit uint64) (domains []string, nv protocol.NumberOfVersion, err protocol.Error)
}
