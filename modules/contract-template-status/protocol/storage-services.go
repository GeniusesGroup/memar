/* For license and copyright information please see the LEGAL file in the code repository */

package cts

import (
	"memar/protocol"

	csp "org/modules/content-status/protocol"
	ctp "org/modules/contract-template/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(contractTemplateID ctp.ContractTemplateUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(contractTemplateID ctp.ContractTemplateUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FilterByStatus(status csp.Status, offset, limit uint64) (contractTemplateIDs []ctp.ContractTemplateUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
