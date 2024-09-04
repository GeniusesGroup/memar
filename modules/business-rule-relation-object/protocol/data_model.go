/* For license and copyright information please see the LEGAL file in the code repository */

package rap

import (
	aa_p "org/modules/app-audit/protocol"
	object_p "org/modules/object/protocol"
	org_p "org/modules/org/protocol"
	storage_p "org/modules/storage/protocol"
)

// Use to store logic on DSLs or portable binaries like WASM, ...
type DataModel interface {
	org_p.Field_OrganizationID
	object_p.Field_ObjectID

	aa_p.Field_AuditRequest
	storage_p.Field_SaveTime
}
