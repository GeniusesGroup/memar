/* For license and copyright information please see the LEGAL file in the code repository */

package tax_p

import (
	aa_p "org/modules/app-audit/protocol"
	society_p "org/modules/society/protocol"
	storage_p "org/modules/storage/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	Field_TaxID
	society_p.Field_SocietyID
	Type() Type

	aa_p.Field_AuditRequest
	storage_p.Field_SaveTime
}
