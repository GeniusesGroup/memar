/* For license and copyright information please see the LEGAL file in the code repository */

package inventory_p

import (
	ut16 "memar/identifier/uuid-time-16byte"
)

type Field_InventoryID interface {
	InventoryID() InventoryUUID
}

// InventoryUUID
type InventoryUUID ut16.UUID
