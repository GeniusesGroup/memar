/* For license and copyright information please see the LEGAL file in the code repository */

package account_p

import (
	quiddity_p "org/modules/identity/quiddity/protocol"
)

type Field_FinancialAccountID interface {
	FinancialAccountID() UUID
}

type UUID quiddity_p.UUID
