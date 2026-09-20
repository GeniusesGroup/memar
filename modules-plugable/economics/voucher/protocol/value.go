/* For license and copyright information please see the LEGAL file in the code repository */

package voucher

import (
	fc_p "org/modules/economics/currency/protocol"
)

type Value interface {
	Field_Each
	Field_Proportion
	Field_Worth
	fc_p.Field_FinancialCurrencyID
}
