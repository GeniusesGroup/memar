/* For license and copyright information please see the LEGAL file in the code repository */

package ctp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	lp "org/modules/law/protocol"
)

// DataModel indicate the domain record data fields.
// 3 type of content exist: 1:about persons, 2:about events, 3:about sciences
type DataModel interface {
	ContentTypeID() ContentTypeUUID
	DomainID() protocol.MediaTypeID // TODO:::
	LawID() lp.LawUUID

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
