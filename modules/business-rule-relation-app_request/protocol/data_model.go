/* For license and copyright information please see the LEGAL file in the code repository */

package brrar_p

import (
	aa_p "org/modules/app-audit/protocol"
	br_p "org/modules/business-rule/protocol"
	storage_p "org/modules/storage/protocol"
)

// Store to know all request created by specific rule.
type DataModel interface {
	br_p.Field_BusinessRuleID
	// TODO::: Is it ok to let a rule make more than one request??
	RequestIndex() uint32
	aa_p.Field_AuditRequest

	storage_p.Field_SaveTime
}
