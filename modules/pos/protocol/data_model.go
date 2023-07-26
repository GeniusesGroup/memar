/* For license and copyright information please see the LEGAL file in the code repository */

// POS or point-of-sale
package pp

import (
	"memar/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	PosID() PosUUID
	Type() Type

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
