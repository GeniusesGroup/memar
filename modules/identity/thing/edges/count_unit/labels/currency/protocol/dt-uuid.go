/* For license and copyright information please see the LEGAL file in the code repository */

package currency_p

import (
	thing_p "org/modules/identity/thing/protocol"
)

type Field_FinancialCurrencyID interface {
	FinancialCurrencyID() UUID
}

type UUID thing_p.UUID
