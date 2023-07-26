/* For license and copyright information please see the LEGAL file in the code repository */

package esp

import (
	"memar/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(areaID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(areaID [16]byte, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FilterByStatus(status Status, offset, limit uint64) (areaIDs [][16]byte, err protocol.Error)

	// protocol.EventTarget
}
