/* For license and copyright information please see the LEGAL file in the code repository */

package cttp

import (
	"memar/protocol"

	ctp "org/modules/contract-template/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(contractTemplateID ctp.ContractTemplateUUID, languages protocol.Language) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(contractTemplateID ctp.ContractTemplateUUID, languages protocol.Language, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	ListLanguages(contractTemplateID ctp.ContractTemplateUUID, offset, limit uint64) (languages []protocol.Language, nv protocol.NumberOfVersion, err protocol.Error)
}
