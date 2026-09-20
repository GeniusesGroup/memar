/* For license and copyright information please see the LEGAL file in the code repository */

package ssp

import (
	error_p "memar/process/error/protocol"

	storage_p "memar/storage/protocol"
	sp "org/modules/management/staff/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv storage_p.NumberOfVersion, err error_p.Error)

	Count(staffID sp.UUID) (nv storage_p.NumberOfVersion, err error_p.Error)
	Get(staffID sp.UUID, vo storage_p.VersionOffset) (dm DataModel, nv storage_p.NumberOfVersion, err error_p.Error)
}
