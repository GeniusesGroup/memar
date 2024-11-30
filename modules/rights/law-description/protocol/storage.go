/* For license and copyright information please see the LEGAL file in the code repository */

package ldp

import (
	error_p "memar/error/protocol"

	lgp "org/modules/knowledge/language/protocol"
	lp "org/modules/rights/law/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv storage_p.NumberOfVersion, err error_p.Error)

	Count(lawID lp.UUID, language lgp.LanguageUUID) (nv storage_p.NumberOfVersion, err error_p.Error)
	Get(lawID lp.UUID, language lgp.LanguageUUID, vo storage_p.VersionOffset) (dm DataModel, nv storage_p.NumberOfVersion, err error_p.Error)

	ListLanguages(lawID lp.UUID, offset, limit uint64) (languages []lgp.LanguageUUID, nv storage_p.NumberOfVersion, err error_p.Error)
}
