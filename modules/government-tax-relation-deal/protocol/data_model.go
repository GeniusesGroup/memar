/* For license and copyright information please see the LEGAL file in the code repository */

package trd_p

import (
	aa_p "org/modules/app-audit/protocol"
	deal_p "org/modules/deal/protocol"
	fm_p "org/modules/financial-money/protocol"
	tax_p "org/modules/government-tax/protocol"
	storage_p "org/modules/storage/protocol"
)

// DataModel indicate the domain record data fields. each order is immutable record.
type DataModel interface {
	deal_p.Field_DealID
	tax_p.Field_TaxID
	fm_p.Field_Amount

	aa_p.Field_AuditRequest
	storage_p.Field_SaveTime
}
