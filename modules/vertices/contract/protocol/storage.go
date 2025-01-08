/* For license and copyright information please see the LEGAL file in the code repository */

package contract_p

import (
	error_p "memar/error/protocol"

	text_p "org/modules/knowledge/text/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

type StorageServices interface {
	Save(c DataModel) (err error_p.Error)

	Get(contractID UUID) (c DataModel, err error_p.Error)

	FindByText(tID text_p.UUID, offset, limit uint64) (contractIDs []UUID, nv storage_p.NumberOfVersion, err error_p.Error)
	// FindByData(data string, offset, limit uint64) (contractsID []UUID, nv storage_p.NumberOfVersion, err error_p.Error)
}
