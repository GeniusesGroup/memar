/* For license and copyright information please see the LEGAL file in the code repository */

package text_p

import (
	error_p "memar/process/error/protocol"

	storage_p "memar/storage/protocol"
	language_p "org/modules/knowledge/language-human/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv storage_p.NumberOfVersion, err error_p.Error)

	Count(textID UUID, language language_p.UUID) (nv storage_p.NumberOfVersion, err error_p.Error)
	Get(textID UUID, language language_p.UUID, vo storage_p.VersionOffset) (dm DataModel, nv storage_p.NumberOfVersion, err error_p.Error)

	// FIND_TextIDs_BY_Text(text string, offset, limit uint64) (textIDs []UUID, nv storage_p.NumberOfVersion, err error_p.Error)

	ListLanguages(textID UUID, offset, limit uint64) (languages []language_p.UUID, nv storage_p.NumberOfVersion, err error_p.Error)
}
