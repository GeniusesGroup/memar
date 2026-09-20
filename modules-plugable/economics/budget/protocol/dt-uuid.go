/* For license and copyright information please see the LEGAL file in the code repository */

package budget_p

import (
	account_p "org/modules/economics/account/protocol"
)

type Field_BudgetID interface {
	BudgetID() UUID
}

type Field_BudgetsID interface {
	BudgetsID() []UUID
}

type UUID account_p.UUID
