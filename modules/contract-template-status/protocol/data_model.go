/* For license and copyright information please see the LEGAL file in the code repository */

package cts

import (
	"libgo/protocol"

	ctp "org/modules/contract-template/protocol"
	qsp "org/modules/quiddity-status/protocol"
	urp "org/modules/user-request/protocol"
)

type DataModel interface {
	ContractTemplateID() ctp.ContractTemplateUUID //
	Status() Status             //
	SaveTime() protocol.Time                      //
	RequestID() urp.UserRequestUUID               //
}

type Statusqsp.Quiddity_Status

const (
	ContractTemplate_Status_Draft = ContractTemplate_Status(qsp.Quiddity_Status_FreeFlag << iota)
)
