/* For license and copyright information please see the LEGAL file in the code repository */

package rsp

import (
	aa_p "org/modules/app-audit/protocol"
	skill_p "org/modules/learn-skill/protocol"
	role_p "org/modules/role/protocol"
	storage_p "org/modules/storage/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	role_p.Field_RoleID
	skill_p.Field_SkillID

	aa_p.Field_AuditRequest
	storage_p.Field_SaveTime
}
