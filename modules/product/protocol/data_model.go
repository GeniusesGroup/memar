/* For license and copyright information please see the LEGAL file in the code repository */

package pp

import (
	"memar/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ProductID() ProductUUID
	Type() Type

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
