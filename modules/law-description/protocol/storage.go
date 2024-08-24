/* For license and copyright information please see the LEGAL file in the code repository */

package ldp

import (
	"memar/protocol"

	lp "org/modules/law/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(lawID lp.LawUUID, language protocol.Language) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(lawID lp.LawUUID, language protocol.Language, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	ListLanguages(lawID lp.LawUUID, offset, limit uint64) (languages []protocol.Language, nv protocol.NumberOfVersion, err protocol.Error)
}
