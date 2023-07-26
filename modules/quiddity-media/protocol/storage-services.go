/* For license and copyright information please see the LEGAL file in the code repository */

package qmp

import (
	"memar/protocol"

	op "org/modules/object/protocol"
	qp "org/modules/quiddity/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(quiddityID qp.QuiddityUUID, priority uint64) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(quiddityID qp.QuiddityUUID, priority uint64, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	ListMedias(quiddityID qp.QuiddityUUID, offset, limit uint64) (objectIDs []op.ObjectUUID, nv protocol.NumberOfVersion, err protocol.Error)
	ListRelates(objectID op.ObjectUUID, offset, limit uint64) (quiddityIDs []qp.QuiddityUUID, nv protocol.NumberOfVersion, err protocol.Error)
	ListPriorities(objectID op.ObjectUUID, quiddityID qp.QuiddityUUID, offset, limit uint64) (priorities []uint64, nv protocol.NumberOfVersion, err protocol.Error)
}
