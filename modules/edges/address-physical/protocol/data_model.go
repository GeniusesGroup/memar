/* For license and copyright information please see the LEGAL file in the code repository */
package ggarp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	gap "org/modules/geography-address/protocol"
)

type DataModel interface {
	AddressID() gap.AddressUUID
	Continent() string
	Country() string
	State() string
	Province() string
	Region() string
	City() string
	District() string
	Boulevard() string
	MainStreet() string
	Street() string
	MainAlley() string
	Alley() string
	Building() string
	Block() string
	Postal() uint32
	ZipCode() uint32

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
