/* For license and copyright information please see the LEGAL file in the code repository */

package ctp

import (
	"memar/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(contractTemplateID ContractTemplateUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(contractTemplateID ContractTemplateUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)
}
