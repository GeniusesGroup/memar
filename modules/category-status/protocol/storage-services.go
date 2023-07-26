/* For license and copyright information please see the LEGAL file in the code repository */

package csp

import (
	"memar/protocol"

	cp "org/modules/category/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(categoryID cp.CategoryUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(categoryID cp.CategoryUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FILTER_CategoryIDs_BY_Status(status Status, offset, limit uint64) (categoryIDs []cp.CategoryUUID, nv protocol.NumberOfVersion, err protocol.Error)

	protocol.EventTarget
}
