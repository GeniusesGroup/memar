/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type ContractStatus interface {
	ContractID() ContractUUID       //
	Status() Contract_Status        //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type Contract_Status Quiddity_Status

const (
	Contract_Status_Negotiation = Contract_Status(Quiddity_Status_FreeFlag << iota)
	Contract_Status_PartlySigned
	Contract_Status_Signed
	Contract_Status_LegalAction
	Contract_Status_Done
	Contract_Status_Canceled
)
