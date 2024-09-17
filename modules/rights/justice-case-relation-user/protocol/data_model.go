/* For license and copyright information please see the LEGAL file in the code repository */

package jcru_p

import (
	aa_p "org/modules/app-audit/protocol"
	jc_p "org/modules/government-justice-case/protocol"
	storage_p "org/modules/storage/protocol"
	user_p "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	jc_p.Field_JusticeCaseID
	user_p.Field_UserID
	Field_RelationType
	// Types of responsibility, including relative or joint liability

	aa_p.Field_AuditRequest
	storage_p.Field_SaveTime
}
