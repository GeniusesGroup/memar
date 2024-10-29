/* For license and copyright information please see the LEGAL file in the code repository */

package contract_p

import (
	quiddity_p "org/modules/identity/quiddity/protocol"
)

type Field_ContractID interface {
	ContractID() UUID
}

type UUID quiddity_p.UUID
