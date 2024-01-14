/* For license and copyright information please see the LEGAL file in the code repository */

package ltp

import (
	"memar/protocol"

	aap "org/modules/app-audit/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	TextID() TextUUID // Wil be unique in all languages
	Language() protocol.Language
	Text() Text

	aap.AuditRequest
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
