/* For license and copyright information please see the LEGAL file in the code repository */

package ldp

import (
	"memar/protocol"

	lp "org/modules/law/protocol"
)

// DataModel
// users can discuss by send suggestion or change proposal with comments to any part of text.
type DataModel interface {
	LawID() lp.LawUUID
	Language() protocol.Language
	Law() string                // HTML, CSS
	Goal() string               // HTML, CSS
	Explanation() string        // HTML, CSS
	ExecutiveGuarantee() string // HTML, CSS
	Technical() string          // HTML, CSS, computer codes or description how to code

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
