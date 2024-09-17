/* For license and copyright information please see the LEGAL file in the code repository */

package bsrm_p

import (
	aa_p "org/modules/app-audit/protocol"
	bm_p "org/modules/business-module/protocol"
	bs_p "org/modules/business-service/protocol"
	storage_p "org/modules/storage/protocol"
)

// DataModel indicates the domain record data fields.
type DataModel interface {
	bs_p.Field_ServiceID
	bm_p.Field_ModuleID
	// Type()

	aa_p.Field_AuditRequest
	storage_p.Field_SaveTime
}
