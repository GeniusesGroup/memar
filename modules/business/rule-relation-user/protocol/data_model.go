/* For license and copyright information please see the LEGAL file in the code repository */

package rap

import (
	aa_p "org/modules/app-audit/protocol"
	br_p "org/modules/business-rule/protocol"
	storage_p "org/modules/storage/protocol"
	user_p "org/modules/user/protocol"
)

type DataModel interface {
	user_p.Field_UserID
	// RuleIndex() IndexID
	br_p.Field_BusinessRuleID

	aa_p.Field_AuditRequest
	storage_p.Field_SaveTime
}
