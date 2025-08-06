/* For license and copyright information please see the LEGAL file in the code repository */

package item_p

import (
	quiddity_p "org/modules/identity/quiddity/protocol"
)

type Field_InvoiceItemID interface {
	// CAN use for other domain too e.g. `calendar`
	InvoiceItemID() UUID
}

type UUID quiddity_p.UUID
