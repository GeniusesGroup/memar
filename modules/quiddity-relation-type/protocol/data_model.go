/* For license and copyright information please see the LEGAL file in the code repository */

package qrtp

import (
	"memar/protocol"
)

// DataModel store some key/value for a Quiddity to describe it e.g. mobile-cpu, ...
// e.g. MetricUnit: Number, Gram, Liter, Second
type DataModel interface {
	TypeID() QuiddityRelationTypeUUID
	Status() Status

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
