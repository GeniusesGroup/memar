/* For license and copyright information please see the LEGAL file in the code repository */

package warehouse_p

import (
	estate_p "org/modules/identity/estate/protocol"
)

type Field_WarehouseID interface {
	WarehouseID() UUID
}

type UUID estate_p.UUID
