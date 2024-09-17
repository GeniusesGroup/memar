/* For license and copyright information please see the LEGAL file in the code repository */

package lwp

import (
	"memar/protocol"

	aap "org/modules/app-audit/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	WordID() WordUUID
	Word() Word

	aap.AuditRequest
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
