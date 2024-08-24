/* For license and copyright information please see the LEGAL file in the code repository */

package ltp

import (
	"memar/protocol"

	lp "org/modules/language/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(textID TextUUID, language lp.LanguageUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(textID TextUUID, language lp.LanguageUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	// FIND_TextIDs_BY_Text(text string, offset, limit uint64) (textIDs []TextUUID, nv protocol.NumberOfVersion, err protocol.Error)

	ListLanguages(textID TextUUID, offset, limit uint64) (languages []lp.LanguageUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
