/* For license and copyright information please see the LEGAL file in the code repository */

package cttp

import (
	"libgo/protocol"

	ctp "org/modules/contract-template/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(contractTemplateID ctp.ContractTemplateUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(contractTemplateID ctp.ContractTemplateUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	ListTags(contractTemplateID ctp.ContractTemplateUUID, offset, limit uint64) (tags []string, nv protocol.NumberOfVersion, err protocol.Error)
	ListContractTemplates(tag string, offset, limit uint64) (contractTemplateIDs []ctp.ContractTemplateUUID, nv protocol.NumberOfVersion, err protocol.Error)

	FilterByStatus(contractTemplateID ctp.ContractTemplateUUID, status Status, offset, limit uint64) (tags []string, nv protocol.NumberOfVersion, err protocol.Error)
}
