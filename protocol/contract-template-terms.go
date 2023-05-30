/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type ContractTemplateTerms interface {
	ContractTemplateID() ContractTemplateUUID //
	Language() protocol.Language              //
	Terms() []string                          // HTML, CSS, JS base, Solidity PL is other option
	Time() protocol.Time                      // save time
	RequestID() urp.UserRequestUUID           //
}

type ContractTemplateTerms_StorageServices interface {
	Save(ct ContractTemplateTerms) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(contractTemplateID [16]byte, languages protocol.Language) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(contractTemplateID [16]byte, languages protocol.Language, vo protocol.VersionOffset) (ct ContractTemplateTerms, nv protocol.NumberOfVersion, err protocol.Error)

	ListLanguages(contractTemplateID [16]byte, offset, limit uint64) (languages []protocol.Language, nv protocol.NumberOfVersion, err protocol.Error)
}
