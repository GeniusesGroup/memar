/* For license and copyright information please see the LEGAL file in the code repository */

package ptip

import (
	error_p "memar/process/error/protocol"

	storage_p "memar/storage/protocol"
	pp "org/modules/economics/product/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv storage_p.NumberOfVersion, err error_p.Error)

	Count(productID pp.UUID) (nv storage_p.NumberOfVersion, err error_p.Error)
	Get(productID pp.UUID, vo storage_p.VersionOffset) (dm DataModel, nv storage_p.NumberOfVersion, err error_p.Error)
}
