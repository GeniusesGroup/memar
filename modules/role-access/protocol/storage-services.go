/* For license and copyright information please see the LEGAL file in the code repository */

package rap

import (
	"memar/protocol"

	rp "org/modules/role/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(roleID rp.RoleUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(roleID rp.RoleUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)
}
