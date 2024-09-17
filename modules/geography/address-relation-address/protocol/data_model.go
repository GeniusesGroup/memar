/* For license and copyright information please see the LEGAL file in the code repository */

package ggara

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	gar "org/modules/geography-address/protocol"
	lp "org/modules/label/protocol"
)

type DataModel interface {
	AddressID() gar.AddressUUID
	RelateAddressID() gar.AddressUUID
	RelationType() lp.LabelUUID

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
