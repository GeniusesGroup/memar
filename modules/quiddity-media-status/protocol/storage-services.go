/* For license and copyright information please see the LEGAL file in the code repository */

package qmsp

import (
	"libgo/protocol"

	op "org/modules/object/protocol"
	qp "org/modules/quiddity/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(quiddityID qp.QuiddityUUID, objectID op.ObjectUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(quiddityID qp.QuiddityUUID, objectID op.ObjectUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)
}
