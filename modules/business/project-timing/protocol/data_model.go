/* For license and copyright information please see the LEGAL file in the code repository */

package ptp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	pp "org/modules/project/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ProjectID() pp.ProjectUUID
	ExpectedTime() protocol.Time
	Deadline() protocol.Time

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
