/* For license and copyright information please see the LEGAL file in the code repository */

package qtp

import (
	"memar/protocol"

	qp "org/modules/quiddity/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(quiddityID qp.QuiddityUUID, language protocol.Language) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(quiddityID qp.QuiddityUUID, language protocol.Language, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	// FIND_QuiddityIDs_BY_Text(text string, offset, limit uint64) (quiddityIDs []qp.QuiddityUUID, nv protocol.NumberOfVersion, err protocol.Error)

	ListQuiddityLanguages(quiddityID qp.QuiddityUUID, offset, limit uint64) (languages []protocol.Language, nv protocol.NumberOfVersion, err protocol.Error)
}
