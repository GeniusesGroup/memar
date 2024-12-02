/* For license and copyright information please see the LEGAL file in the code repository */

package fsp_p

import (
	error_p "memar/error/protocol"

	form_p "org/modules/knowledge/form/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv storage_p.NumberOfVersion, err error_p.Error)

	Count(formID form_p.UUID) (nv storage_p.NumberOfVersion, err error_p.Error)
	Get(formID form_p.UUID, vo storage_p.VersionOffset) (dm DataModel, nv storage_p.NumberOfVersion, err error_p.Error)
}
