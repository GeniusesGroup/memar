/* For license and copyright information please see the LEGAL file in the code repository */

package ggcap

import (
	"memar/protocol"
	ggcp "org/modules/geography-coordinate/protocol"
)

type DataModel interface {
	CoordinateID() ggcp.CoordinateUUID
	Distance() uint64     // km or ...
	AverageSpeed() uint64 // km/h or ...

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
