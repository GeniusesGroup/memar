/* For license and copyright information please see the LEGAL file in the code repository */

package ctp

import (
	"memar/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(tag string) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(tag string, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	// TODO:::
}
