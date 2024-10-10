/* For license and copyright information please see the LEGAL file in the code repository */

package voucher

import (
	invoice_p "org/modules/financial/invoice/protocol"
	money_p "org/modules/financial/money/protocol"
)

type Invoice_Condition interface {
	Field_Each
	MinPrice() money_p.Amount // Minimum invoice price, currency depend on voucher value
	MinAmount() uint64        // Minimum invoice product numbers
}

type Invoice_ID interface {
	invoice_p.Field_InvoiceID
}

type Invoice_Type interface {
	Field_InvoiceType
}

type Invoice_MaxUsage interface {
	MaximumInvoice() uint64
}
