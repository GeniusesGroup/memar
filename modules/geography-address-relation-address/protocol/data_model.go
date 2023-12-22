/* For license and copyright information please see the LEGAL file in the code repository */

package ggara

import (
	"memar/protocol"
	ggr "org/modules/geography-address/protocol"
	ggrrl "org/modules/geography-region-relation-label/protocol"
)

type DataModel interface {
	AddressID() ggr.AddressUUID
	RelateAdddressID() ggr.AddressUUID
	RelationType() ggrrl.label

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
