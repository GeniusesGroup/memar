/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"memar/math/per"
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	cp "org/modules/contract/protocol"
)

type ContractExpertOpinion interface {
	ContractID() cp.ContractUUID
	ExpertID() [16]byte
	Opinion() string
	Progress() per.Myriad

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
