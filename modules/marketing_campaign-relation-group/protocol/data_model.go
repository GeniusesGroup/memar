/* For license and copyright information please see the LEGAL file in the code repository */

/*
- To send SMS or ... to all user joined group. Join can be optional. DeJoin mechanism must be exist.
*/
package mcrgp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
)

type DataModel interface {
	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
