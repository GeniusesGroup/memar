/* For license and copyright information please see the LEGAL file in the code repository */

package tax_p

import (
	ut16 "memar/identifier/uuid-time-16byte"
)

type Field_TaxID interface {
	TaxID() TaxUUID
}

type TaxUUID ut16.UUID
