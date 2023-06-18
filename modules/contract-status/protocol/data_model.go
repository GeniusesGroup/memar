/* For license and copyright information please see the LEGAL file in the code repository */

package csp

import (
	"libgo/protocol"

	cp "org/modules/contract/protocol"
	qsp "org/modules/quiddity-status/protocol"
	urp "org/modules/user-request/protocol"
)

type DataModel interface {
	ContractID() cp.ContractUUID    //
	Status() Status                 //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Status qsp.Quiddity_Status

const (
	Status_Negotiation = Status(qsp.Quiddity_Status_FreeFlag << iota)
	Status_PartlySigned
	Status_Signed
	Status_LegalAction
	Status_Done
	Status_Canceled
)
