/* For license and copyright information please see the LEGAL file in the code repository */

package rlp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	eblp "org/modules/estate-building-location/protocol"
	rp "org/modules/role/protocol"
)

// DataModel indicate the domain record data fields.
// Let staffs register enter and exit time by their mobiles in specific location.
type DataModel interface {
	RoleID() rp.RoleUUID
	BuildingLocationID() eblp.BuildingLocationUUID
	Status() Status

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
