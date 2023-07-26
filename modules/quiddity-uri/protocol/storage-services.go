/* For license and copyright information please see the LEGAL file in the code repository */

package qup

import (
	"memar/protocol"

	qp "org/modules/quiddity/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(uri []byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(uri []byte, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FindByQuiddity(quiddityID qp.QuiddityUUID, offset, limit uint64) (uris [][]byte, nv protocol.NumberOfVersion, err protocol.Error)
}
