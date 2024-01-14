/* For license and copyright information please see the LEGAL file in the code repository */

package tvp

import (
	"memar/math/per"
	"memar/protocol"

	aap "org/modules/app-audit/protocol"
	tp "org/modules/tax/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	TaxID() tp.TaxUUID
	Value() per.Myriad

	aap.AuditRequest
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
