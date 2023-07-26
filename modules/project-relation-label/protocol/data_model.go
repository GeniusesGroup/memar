/* For license and copyright information please see the LEGAL file in the code repository */

package prlp

import (
	"memar/protocol"

	lp "org/modules/label/protocol"
	pp "org/modules/project/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ProjectID() pp.ProjectUUID
	LabelID() lp.LabelUUID

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
