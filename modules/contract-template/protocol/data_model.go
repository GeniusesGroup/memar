/* For license and copyright information please see the LEGAL file in the code repository */

package ctp

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)



type DataMdoel interface {
	ContractTemplateID() ContractTemplateUUID //
	Language() protocol.Language              // base language
	SaveTime() protocol.Time                  //
	RequestID() urp.UserRequestUUID           //
}

