/* For license and copyright information please see the LEGAL file in the code repository */

package form_p

import (
	error_p "memar/error/protocol"

	storage_p "org/modules/storage/primitive/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv storage_p.NumberOfVersion, err error_p.Error)

	Count(formID UUID) (nv storage_p.NumberOfVersion, err error_p.Error)
	Get(formID UUID, vo storage_p.VersionOffset) (dm DataModel, nv storage_p.NumberOfVersion, err error_p.Error)

	FIND_FormIDs_By_Type(formID UUID, t Type, offset, limit uint64) (nv storage_p.NumberOfVersion, err error_p.Error)
}
