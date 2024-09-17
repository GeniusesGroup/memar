/* For license and copyright information please see the LEGAL file in the code repository */

package lwsp

import (
	"memar/protocol"

	aap "org/modules/app-audit/protocol"
	lwp "org/modules/language-word/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	WordID() lwp.WordUUID
	Status() Status

	aap.AuditRequest
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
