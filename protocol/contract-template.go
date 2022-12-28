/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

type ContractTemplate interface {
	ContractTemplateID() [16]byte // contract-template domain
	Language() protocol.Language  // base language
	Time() protocol.Time          // save time
	RequestID() UserRequestUUID   // user-request domain
}

type ContractTemplate_StorageServices interface {
	Save(ct ContractTemplate) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(contractTemplateID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(contractTemplateID [16]byte, vo protocol.VersionOffset) (ct ContractTemplate, nv protocol.NumberOfVersion, err protocol.Error)
}
