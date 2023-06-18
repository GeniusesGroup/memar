/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	cp "org/modules/contract/protocol"
)

type ContractExpertOpinion interface {
	ContractID() cp.ContractUUID    //
	ExpertID() [16]byte             //
	Opinion() string                //
	Progress() protocol.PerMyriad   //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
