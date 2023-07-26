/* For license and copyright information please see the LEGAL file in the code repository */

package ctp

import (
	"memar/protocol"

	lp "org/modules/law/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(contentTypeID ContentTypeUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(contentTypeID ContentTypeUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FindByLaw(lawID lp.LawUUID, offset, limit uint64) (contentTypeIDs []ContentTypeUUID, nv protocol.NumberOfVersion, err protocol.Error)
	GetIDs(offset, limit uint64) (contentTypeIDs []ContentTypeUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
