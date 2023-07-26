/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"memar/protocol"
)

type StorageServices interface {
	Save(gc GUICategories) (nv protocol.NumberOfVersion, err protocol.Error)

	Count() (nv protocol.NumberOfVersion, err protocol.Error)
	Get(vo protocol.VersionOffset) (gc GUICategories, nv protocol.NumberOfVersion, err protocol.Error)
}
