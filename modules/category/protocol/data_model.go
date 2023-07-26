/* For license and copyright information please see the LEGAL file in the code repository */

package cp

import (
	"memar/protocol"
)

// DataModel indicate the domain record data fields.
// DataModel or Topic
type DataModel interface {
	CategoryID() CategoryUUID
	ParentID() CategoryUUID // Exist if it isn't top category.

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
