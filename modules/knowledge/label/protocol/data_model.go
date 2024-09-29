/* For license and copyright information please see the LEGAL file in the code repository */

package label_p

import (
	audit_p "org/modules/computer/audit/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	Field_LabelID
	// Field_Status

	audit_p.Field_RequestID
	storage_p.Field_SaveTime
}
