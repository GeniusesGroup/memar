/* For license and copyright information please see the LEGAL file in the code repository */

package contract_p

import (
	error_p "memar/error/protocol"

	ctp "org/modules/rights/contract-template/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

type StorageServices interface {
	Save(c DataModel) (err error_p.Error)

	Get(contractID UUID, vo storage_p.VersionOffset) (c DataModel, err error_p.Error)

	FindByContractTemplate(contractTemplateID ctp.UUID, offset, limit uint64) (contractIDs []UUID, nv storage_p.NumberOfVersion, err error_p.Error)
	// FindByData(data string, offset, limit uint64) (contractsID []UUID, nv storage_p.NumberOfVersion, err error_p.Error)
}
