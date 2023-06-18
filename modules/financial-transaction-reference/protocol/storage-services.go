/* For license and copyright information please see the LEGAL file in the code repository */

package ftrp

import (
	"libgo/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(referenceID protocol.UUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(referenceID protocol.UUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)
}
