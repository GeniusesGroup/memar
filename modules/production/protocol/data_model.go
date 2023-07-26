/* For license and copyright information please see the LEGAL file in the code repository */

package pp

import (
	"memar/protocol"
)

// DataModel is the structure of production line.
// https://www.zenscale.in/planning
type DataModel interface {
	ProductionID() ProductionUUID
	Type() Type
	Status() Status

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
