/* For license and copyright information please see the LEGAL file in the code repository */

package cttp

import (
	"libgo/protocol"

	ctp "org/modules/contract-template/protocol"
	urp "org/modules/user-request/protocol"
)

type DataModel interface {
	ContractTemplateID() ctp.ContractTemplateUUID //
	Language() protocol.Language                  //
	Terms() []string                              // HTML, CSS, JS base, Solidity PL is other option
	SaveTime() protocol.Time                      //
	RequestID() urp.UserRequestUUID               //
}

