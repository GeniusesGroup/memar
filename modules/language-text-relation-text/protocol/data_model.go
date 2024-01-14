/* For license and copyright information please see the LEGAL file in the code repository */

package ltrtp

import (
	"memar/protocol"

	aap "org/modules/app-audit/protocol"
	ltp "org/modules/language-text/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	TextID() ltp.TextUUID
	RelatedID() ltp.TextUUID
	Ranking() uint64
	Type() Type

	aap.AuditRequest
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
