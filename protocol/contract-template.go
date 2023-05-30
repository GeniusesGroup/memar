/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type ContractTemplateUUID = protocol.UUID

type ContractTemplate interface {
	ContractTemplateID() ContractTemplateUUID //
	Language() protocol.Language              // base language
	Time() protocol.Time                      // save time
	RequestID() urp.UserRequestUUID           //
}

type ContractTemplate_StorageServices interface {
	Save(ct ContractTemplate) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(contractTemplateID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(contractTemplateID [16]byte, vo protocol.VersionOffset) (ct ContractTemplate, nv protocol.NumberOfVersion, err protocol.Error)
}
