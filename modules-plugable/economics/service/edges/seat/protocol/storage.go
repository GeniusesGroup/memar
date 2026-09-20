/* For license and copyright information please see the LEGAL file in the code repository */

package psp

import (
	error_p "memar/process/error/protocol"

	storage_p "memar/storage/protocol"
	pp "org/modules/economics/product/protocol"
	op "org/modules/storage/object/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv storage_p.NumberOfVersion, err error_p.Error)

	Count(productID pp.UUID) (nv storage_p.NumberOfVersion, err error_p.Error)
	Get(productID pp.UUID, vo storage_p.VersionOffset) (dm DataModel, nv storage_p.NumberOfVersion, err error_p.Error)

	FIND_ProductIDs_BY_MapID(mapID op.UUID, offset, limit uint64) (productIDs []pp.UUID, nv storage_p.NumberOfVersion, err error_p.Error)
	FILTER_ProductIDs_BY_SeatType(t Type, offset, limit uint64) (productIDs []pp.UUID, nv storage_p.NumberOfVersion, err error_p.Error)
}
