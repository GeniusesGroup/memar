/* For license and copyright information please see the LEGAL file in the code repository */

package prpp

import (
	error_p "memar/error/protocol"

	pp "org/modules/business/project/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv storage_p.NumberOfVersion, err error_p.Error)

	Count(projectID pp.UUID, otherID pp.UUID) (nv storage_p.NumberOfVersion, err error_p.Error)
	Get(projectID pp.UUID, otherID pp.UUID, vo storage_p.VersionOffset) (dm DataModel, nv storage_p.NumberOfVersion, err error_p.Error)

	LIST_OtherIDs_BY_ProjectID(projectID pp.UUID, offset, limit uint64) (OtherIDs []pp.UUID, nv storage_p.NumberOfVersion, err error_p.Error)
}
