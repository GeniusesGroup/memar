/* For license and copyright information please see the LEGAL file in the code repository */

package transaction_p

import (
	record_p "memar/storage/record/protocol"
)

type Field_FinancialTransactionUUID interface {
	FinancialTransactionUUID() UUID
}

type UUID record_p.UUID
