/* For license and copyright information please see the LEGAL file in the code repository */

package arp

import (
	"memar/protocol"

	asp "org/modules/app-service/protocol"
	up "org/modules/user/protocol"
)

// Application service request domain use to prove how other records created as a chain to other records or standalone data.

// DataModel indicates the domain record data fields.
type DataModel interface {
	RequestID() RequestUUID
	ServiceID() asp.ServiceUUID
	UserID() up.UserUUID
	UserConnectionID() [16]byte // Store to remember which request belongs to which Connection/AppInstance.
	// TODO::: move to esteghrar repo/connection
	// ClientType() string // persiaos, web, android, ios, ...
	// Geo()                // location of user or post

	protocol.Storage_SaveTime // Request time or save Time of the request not the created record by this record.
}
