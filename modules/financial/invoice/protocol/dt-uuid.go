/* For license and copyright information please see the LEGAL file in the code repository */

package invoice_p

import (
	quiddity_p "org/modules/identity/quiddity/protocol"
)

type Field_InvoiceID interface {
	InvoiceID() UUID
}

type UUID quiddity_p.UUID
