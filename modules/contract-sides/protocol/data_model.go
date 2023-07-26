/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"memar/protocol"

	cp "org/modules/contract/protocol"
	up "org/modules/user/protocol"
)

type ContractSides interface {
	ContractID() cp.ContractUUID
	SideType() SideType
	UserID() up.UserUUID // Can be any user type e.g. staff
	UserSignature() []byte

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
