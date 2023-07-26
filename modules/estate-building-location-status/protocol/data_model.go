/* For license and copyright information please see the LEGAL file in the code repository */

package eblsp

import (
	"memar/protocol"

	eblp "org/modules/estate-building-location/protocol"
)

type DataModel interface {
	BuildingLocationID() eblp.BuildingLocationUUID
	Status() Status

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
