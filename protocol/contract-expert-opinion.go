/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

type ContractExpertOpinion interface {
	ContractID() [16]byte         // contract domain
	ExpertID() [16]byte           //
	Opinion() string              //
	Progress() protocol.PerMyriad //
	Time() protocol.Time          // save time
	RequestID() UserRequestUUID   // user-request domain
}
