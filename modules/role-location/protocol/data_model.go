/* For license and copyright information please see the LEGAL file in the code repository */

package rlp

import (
	aa_p "org/modules/app-audit/protocol"
	ebl_p "org/modules/estate-building-location/protocol"
	role_p "org/modules/role/protocol"
	storage_p "org/modules/storage/protocol"
)

// DataModel indicate the domain record data fields.
// Let staffs register enter and exit time by their mobiles in specific location.
type DataModel interface {
	role_p.Field_RoleID
	ebl_p.Field_BuildingLocationID
	Status() Status

	aa_p.Field_AuditRequest
	storage_p.Field_SaveTime
}
