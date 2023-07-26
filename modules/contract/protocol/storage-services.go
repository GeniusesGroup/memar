/* For license and copyright information please see the LEGAL file in the code repository */

package cp

import (
	"memar/protocol"

	ctp "org/modules/contract-template/protocol"
)

type StorageServices interface {
	Save(c DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(contractID ContractUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(contractID ContractUUID, vo protocol.VersionOffset) (c DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FindByContractTemplate(contractTemplateID ctp.ContractTemplateUUID, offset, limit uint64) (contractIDs []ContractUUID, nv protocol.NumberOfVersion, err protocol.Error)
	FindByData(data string, offset, limit uint64) (contractIDs ContractUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
