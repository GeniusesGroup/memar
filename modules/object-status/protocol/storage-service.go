/* For license and copyright information please see the LEGAL file in the code repository */

package osp

import (
	"memar/protocol"

	op "org/modules/object/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(objectID op.ObjectUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(objectID op.ObjectUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	// FilterByStatus(status Status, offset, limit uint64) (objectIDs []op.ObjectUUID, nv protocol.NumberOfVersion, err protocol.Error)

	// protocol.EventTarget
}
