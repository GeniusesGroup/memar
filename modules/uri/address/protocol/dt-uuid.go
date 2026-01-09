/* For license and copyright information please see the LEGAL file in the code repository */

package address_p

import (
	estate_p "org/modules/identity/estate/protocol"
)

type Field_AddressUUID interface {
	AddressUUID() UUID
}

type UUID estate_p.UUID
