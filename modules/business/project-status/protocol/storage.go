/* For license and copyright information please see the LEGAL file in the code repository */

package psp

import (
	error_p "memar/error/protocol"

	pp "org/modules/business/project/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv storage_p.NumberOfVersion, err error_p.Error)

	Count(projectID pp.UUID) (nv storage_p.NumberOfVersion, err error_p.Error)
	Get(projectID pp.UUID, vo storage_p.VersionOffset) (dm DataModel, nv storage_p.NumberOfVersion, err error_p.Error)
}
