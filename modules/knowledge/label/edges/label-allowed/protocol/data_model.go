/* For license and copyright information please see the LEGAL file in the code repository */

package la_p

import (
	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"

	module_p "org/modules/computer/module/protocol"
	status_p "org/modules/fields/status/protocol"
	label_p "org/modules/knowledge/label/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	label_p.Field_LabelUUID

	// always `logic_p.Empty() == false`
	PrimaryNodeModuleID() module_p.UUID
	// `logic_p.Empty() == true` means label can use in `label-relation-other` domain
	SecondaryNodeModuleID() module_p.UUID

	status_p.Field_Status

	request_p.Field_RequestID
	audit_time_p.Field_Request
}
