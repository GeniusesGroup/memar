/* For license and copyright information please see the LEGAL file in the code repository */

package transaction_p

import (
	quiddity_p "org/modules/identity/quiddity/protocol"
)

type Field_FinancialTransactionID interface {
	FinancialTransactionID() UUID
}

type UUID quiddity_p.UUID
