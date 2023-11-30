/* For license and copyright information please see the LEGAL file in the code repository */

package pptp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	pp "org/modules/pos/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	PosID() pp.PosUUID
	// TODO::: VAT number, store address, logo, return rule, ...

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

// sabz.city/complaints?tel=xxxxxxxxxx&orgID=xxx
