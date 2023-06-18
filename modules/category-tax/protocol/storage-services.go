/* For license and copyright information please see the LEGAL file in the code repository */

package csp

import (
	"libgo/protocol"
	cp "org/modules/category/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(categoryID cp.CategoryUUID, SocietyID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(categoryID cp.CategoryUUID, SocietyID [16]byte, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_CategoryIDs_BY_SocietyID(SocietyID [16]byte, offset, limit uint64) (categoryIDs []cp.CategoryUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
