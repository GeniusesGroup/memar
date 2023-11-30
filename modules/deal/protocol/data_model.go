/* For license and copyright information please see the LEGAL file in the code repository */

package dp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields. each order is immutable record.
// use to register an order to e.g. exchange(an instruction to buy or sell) currencies
// A matching engine uses the orders book to determine which orders can be fully or partially executed.
type DataModel interface {
	DealUUID() DealUUID
	UserID() up.UserUUID

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
