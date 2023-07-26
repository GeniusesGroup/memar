/* For license and copyright information please see the LEGAL file in the code repository */

package qtp

import (
	"memar/protocol"

	qp "org/modules/quiddity/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuiddityID() qp.QuiddityUUID // Wil be unique in all languages
	Language() protocol.Language
	Title() Title

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
