/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

type ContractTemplateTerms interface {
	ContractTemplateID() [16]byte // contract-template domain
	Language() protocol.Language  //
	Terms() []string              // HTML, CSS, JS base, Solidity PL is other option
	Time() protocol.Time          // save time
	RequestID() UserRequestUUID   // user-request domain
}

type ContractTemplateTerms_StorageServices interface {
	Save(ct ContractTemplateTerms) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(contractTemplateID [16]byte, languages protocol.Language) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(contractTemplateID [16]byte, languages protocol.Language, vo protocol.VersionOffset) (ct ContractTemplateTerms, nv protocol.NumberOfVersion, err protocol.Error)

	ListLanguages(contractTemplateID [16]byte, offset, limit uint64) (languages []protocol.Language, nv protocol.NumberOfVersion, err protocol.Error)
}
