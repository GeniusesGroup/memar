/* For license and copyright information please see the LEGAL file in the code repository */

package tp

import (
	"memar/protocol"

	aap "org/modules/app-audit/protocol"
	sp "org/modules/society/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	TaxID() TaxUUID
	SocietyID() sp.SocietyUUID
	Type() Type

	aap.AuditRequest
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
