/* For license and copyright information please see the LEGAL file in the code repository */

package ivaudp

import (
	"libgo/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count() (nv protocol.NumberOfVersion, err protocol.Error)
	Get(vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)
}
