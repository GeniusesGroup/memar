/* For license and copyright information please see the LEGAL file in the code repository */

package ctp

import (
	"libgo/protocol"
)

type StorageServices interface {
	Save(ct DataMdoel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(contractTemplateID ContractTemplateUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(contractTemplateID ContractTemplateUUID, vo protocol.VersionOffset) (ct DataMdoel, nv protocol.NumberOfVersion, err protocol.Error)
}
