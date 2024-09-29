/* For license and copyright information please see the LEGAL file in the code repository */

package ls_p

import (
	audit_p "org/modules/computer/audit/protocol"
	label_p "org/modules/knowledge/label/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

type DataModel interface {
	label_p.Field_LabelID
	Field_Status

	audit_p.Field_RequestID
	storage_p.Field_SaveTime
}
