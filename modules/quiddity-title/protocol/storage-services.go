/* For license and copyright information please see the LEGAL file in the code repository */

package qtp

import (
	"libgo/protocol"

	qp "org/modules/quiddity/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(quiddityID qp.QuiddityUUID, language protocol.Language) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(quiddityID qp.QuiddityUUID, language protocol.Language, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	ListQuiddityLanguages(quiddityID qp.QuiddityUUID, offset, limit uint64) (languages []protocol.Language, nv protocol.NumberOfVersion, err protocol.Error)
}
