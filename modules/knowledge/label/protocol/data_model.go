/* For license and copyright information please see the LEGAL file in the code repository */

package lp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	LabelID() LabelUUID
	Status() Status

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
