/* For license and copyright information please see the LEGAL file in the code repository */

package anlp

import (
	"memar/protocol"

	aap "org/modules/app-audit/protocol"
	anp "org/modules/app-node/protocol"
	lp "org/modules/language/protocol"
)

type DataModel interface {
	NodeID() anp.NodeUUID
	Language() lp.LanguageUUID
	Status()

	aap.AuditRequest
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
