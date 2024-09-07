/* For license and copyright information please see the LEGAL file in the code repository */

package bms_p

import (
	aa_p "org/modules/app-audit/protocol"
	app_p "org/modules/app/protocol"
	bm_p "org/modules/business-module/protocol"
	storage_p "org/modules/storage/protocol"
)

type DataModel interface {
	app_p.Field_ApplicationID
	bm_p.Field_ModuleID
	Status()

	aa_p.Field_AuditRequest
	storage_p.Field_SaveTime
}
