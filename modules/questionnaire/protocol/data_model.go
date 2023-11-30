/* For license and copyright information please see the LEGAL file in the code repository */

package qp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuestionnaireID() QuestionnaireUUID
	Type() Type

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

// link to group
