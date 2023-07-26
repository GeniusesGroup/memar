/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"memar/protocol"

	cp "org/modules/coordinate/protocol"
)

type DataModel interface {
	CoordinateID() cp.CoordinateUUID
	Distance() uint64     // km or ...
	AverageSpeed() uint64 // km/h or ...

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
