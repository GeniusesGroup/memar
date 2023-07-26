/* For license and copyright information please see the LEGAL file in the code repository */

package cp

import (
	"memar/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(categoryID CategoryUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(categoryID CategoryUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_CategoryIDs_BY_ParentID(parentID CategoryUUID, offset, limit uint64) (categoryIDs []CategoryUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_ParentIDs_BY_CategoryID(categoryID CategoryUUID, offset, limit uint64) (parentIDs []CategoryUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
