/* For license and copyright information please see the LEGAL file in the code repository */

package qcu_p

import (
	audit_p "org/modules/computer/audit/protocol"
	quiddity_p "org/modules/identity/quiddity/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	quiddity_p.Field_QuiddityID
	Field_CountUnitID
	// TODO::: Allow or need multiple count unit?

	audit_p.Field_RequestID
	storage_p.Field_SaveTime
}
