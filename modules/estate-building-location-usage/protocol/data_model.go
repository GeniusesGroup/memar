/* For license and copyright information please see the LEGAL file in the code repository */

package eblup

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	eblp "org/modules/estate-building-location/protocol"
)

type DataModel interface {
	BuildingLocationID() eblp.BuildingLocationUUID
	Usage() Usage

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
