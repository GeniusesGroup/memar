/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type ContractExpertOpinion interface {
	ContractID() ContractUUID       //
	ExpertID() [16]byte             //
	Opinion() string                //
	Progress() protocol.PerMyriad   //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}
