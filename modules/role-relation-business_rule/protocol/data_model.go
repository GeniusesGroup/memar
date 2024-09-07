/* For license and copyright information please see the LEGAL file in the code repository */

package rrbr_p

import (
	aa_p "org/modules/app-audit/protocol"
	br_p "org/modules/business-rule/protocol"
	role_p "org/modules/role/protocol"
	storage_p "org/modules/storage/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	role_p.Field_RoleID
	br_p.Field_BusinessRuleID
	Field_RelationType

	aa_p.Field_AuditRequest
	storage_p.Field_SaveTime
}
