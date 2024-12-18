/* For license and copyright information please see the LEGAL file in the code repository */

package la_p

import (
	request_p "memar/audit/request/protocol"
	audit_time_p "memar/audit/time/protocol"

	module_p "org/modules/computer/module/protocol"
	org_p "org/modules/identity/org/protocol"
	label_p "org/modules/knowledge/label/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	label_p.Field_LabelID
	// indicate allowed labeling occur in which organization.
	org_p.Field_OrganizationID

	// always `logic_p.Empty() == false`
	PrimaryNodeModuleID() module_p.UUID
	// `logic_p.Empty() == true` means label can use in `label-relation-other` domain
	SecondaryNodeModuleID() module_p.UUID

	Field_Status

	request_p.Field_RequestID
	audit_time_p.Field_SaveTime
}
