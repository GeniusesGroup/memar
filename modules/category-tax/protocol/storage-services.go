/* For license and copyright information please see the LEGAL file in the code repository */

package csp

import (
	"memar/protocol"

	cp "org/modules/category/protocol"
	sp "org/modules/society/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(categoryID cp.CategoryUUID, SocietyID sp.SocietyUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(categoryID cp.CategoryUUID, SocietyID sp.SocietyUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_CategoryIDs_BY_SocietyID(SocietyID sp.SocietyUUID, offset, limit uint64) (categoryIDs []cp.CategoryUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
