/* For license and copyright information please see the LEGAL file in the code repository */

package rrop

import (
	aa_p "org/modules/app-audit/protocol"
	org_p "org/modules/org/protocol"
	role_p "org/modules/role/protocol"
	storage_p "org/modules/storage/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	org_p.Field_OrganizationID
	role_p.Field_RoleID

	aa_p.Field_AuditRequest
	storage_p.Field_SaveTime
}
