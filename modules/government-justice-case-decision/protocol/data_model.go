/* For license and copyright information please see the LEGAL file in the code repository */

package jcd_p

import (
	aa_p "org/modules/app-audit/protocol"
	jcc_p "org/modules/government-justice-case-claim/protocol"
	jc_p "org/modules/government-justice-case/protocol"
	storage_p "org/modules/storage/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	jc_p.Field_JusticeCaseID
	jcc_p.Field_ClaimNumber
	Field_Decision

	aa_p.Field_AuditRequest
	storage_p.Field_SaveTime
}
