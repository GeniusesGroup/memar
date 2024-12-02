/* For license and copyright information please see the LEGAL file in the code repository */

package fr_p

import (
	error_p "memar/error/protocol"

	storage_p "org/modules/storage/primitive/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv storage_p.NumberOfVersion, err error_p.Error)

	Count(formRespondentID UUID) (nv storage_p.NumberOfVersion, err error_p.Error)
	Get(formRespondentID UUID, vo storage_p.VersionOffset) (dm DataModel, nv storage_p.NumberOfVersion, err error_p.Error)
}
