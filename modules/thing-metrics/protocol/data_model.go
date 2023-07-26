/* For license and copyright information please see the LEGAL file in the code repository */

package tmp

import (
	"memar/protocol"

	tp "org/modules/thing/protocol"
)

// each metrics for a thing is immutable record and so use version mechanism to chain metrics for a device.
type DataModel interface {
	ThingID() tp.ThingUUID
	MetricUnit() MetricUnit
	Amount() int64

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
