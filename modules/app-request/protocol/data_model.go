/* For license and copyright information please see the LEGAL file in the code repository */

package arp

import (
	"memar/protocol"

	acp "org/modules/app-connection/protocol"
	asp "org/modules/app-service/protocol"
)

// Application service request domain use to prove how other records created as a chain to other records or standalone data.

// DataModel indicates the domain record data fields.
type DataModel interface {
	RequestID() RequestUUID
	ServiceID() asp.ServiceUUID
	ConnectionID() acp.ConnectionUUID // Store to remember which request belongs to which Connection/AppInstance.

	protocol.Storage_SaveTime // Request time or save Time of the request not the created record by this record.
}
