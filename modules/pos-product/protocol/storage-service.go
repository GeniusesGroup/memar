/* For license and copyright information please see the LEGAL file in the code repository */

package ppp

import (
	"libgo/protocol"

	pp "org/modules/pos/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(posID pp.PosUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(posID pp.PosUUID, vo protocol.VersionOffset) (dm DataModel, err protocol.Error)
}
