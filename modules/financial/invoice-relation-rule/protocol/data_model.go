/* For license and copyright information please see the LEGAL file in the code repository */

package irr_p

import (
	rule_p "org/modules/business/rule/protocol"
	audit_p "org/modules/computer/audit/protocol"
	invoice_p "org/modules/financial/invoice/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	invoice_p.Field_InvoiceID
	rule_p.Field_BusinessRuleID
	Status()

	audit_p.Field_RequestID
	storage_p.Field_SaveTime
}
