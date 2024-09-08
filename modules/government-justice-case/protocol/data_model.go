/* For license and copyright information please see the LEGAL file in the code repository */

package jc_p

import (
	aa_p "org/modules/app-audit/protocol"
	storage_p "org/modules/storage/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	Field_JusticeCaseID
	// TODO::: ??

	aa_p.Field_AuditRequest
	storage_p.Field_SaveTime
}
