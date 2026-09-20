/* For license and copyright information please see the LEGAL file in the code repository */

package salary_p

import (
	currency_p "org/modules/identity/thing/edges/count_unit/labels/currency/protocol"
	fmp "org/modules/economics/money/protocol"
)

// DataModel is fixed base salary that will follow org||department||role salary rules.
type DataModel interface {
	fcp.Field_FinancialCurrencyID
	HourlySalary() fmp.Amount
}
