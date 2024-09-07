/* For license and copyright information please see the LEGAL file in the code repository */

package tv_p

import (
	"memar/math/per"

	aa_p "org/modules/app-audit/protocol"
	tax_p "org/modules/government-tax/protocol"
	storage_p "org/modules/storage/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	tax_p.Field_TaxID
	Value() per.Myriad

	aa_p.Field_AuditRequest
	storage_p.Field_SaveTime
}
