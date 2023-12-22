/* For license and copyright information please see the LEGAL file in the code repository */
package ggarp

import (

	"memar/protocol"
	ggap "org/modules/geography-address/protocol"
	
)

type DataModel interface {

	AddressID() ggap.AddressUUID
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
	Zipcode() uint32

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
