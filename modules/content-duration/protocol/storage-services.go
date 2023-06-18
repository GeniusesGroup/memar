/* For license and copyright information please see the LEGAL file in the code repository */

package cdp

import (
	"libgo/protocol"

	cp "org/modules/content/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(contentID cp.ContentUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(contentID cp.ContentUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)
}
