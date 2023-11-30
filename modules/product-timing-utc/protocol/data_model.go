/* For license and copyright information please see the LEGAL file in the code repository */

package ptup

import (
	"memar/protocol"
	"memar/time/earth"
	"memar/time/utc"

	arp "org/modules/app-request/protocol"
	pp "org/modules/product/protocol"
)

type DataModel interface {
	ProductID() pp.ProductUUID
	Day() utc.DayElapsed
	DayHours() earth.DayHours // what hours in a day this service active to provide services

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
