/* For license and copyright information please see the LEGAL file in the code repository */

package inventory_p

import (
	thing_p "org/modules/identity/thing/protocol"
)

type Field_InventoryID interface {
	InventoryID() UUID
}

// UUID is inventory identification or SKU
type UUID thing_p.UUID
