/* For license and copyright information please see the LEGAL file in the code repository */

package lrop

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	lp "org/modules/label/protocol"
)

// TODO::: Need this domain??

// DataModel indicate the domain record data fields.
type DataModel interface {
	LabelID() lp.LabelUUID
	DomainID() protocol.MediaTypeID
	// TODO::: primary key may not be a single field!
	RecordID() protocol.UUID // in above domain
	Status()

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
