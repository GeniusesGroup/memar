/* For license and copyright information please see the LEGAL file in the code repository */

package contract_p

import (
	group_p "org/modules/organization/group/protocol"
)

type Field_ContractID interface {
	ContractID() UUID
}

// UUID is group to support many functionality like chats, expert opinion, ...
type UUID group_p.UUID
