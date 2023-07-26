/* For license and copyright information please see the LEGAL file in the code repository */

package urp

import (
	"memar/protocol"

	up "org/modules/user/protocol"
)

// DataModel indicates the domain record data fields.
type DataModel interface {
	RequestID() UserRequestUUID      //
	DomainID() protocol.MediaTypeID  // e.g. product, content, ... domain
	ServiceID() protocol.MediaTypeID //
	UserID() up.UserUUID             // user domain
	UserConnectionID() [16]byte      // Store to remember which request belongs to which Connection/AppInstance.
	// TODO::: move to esteghrar repo/connection
	// ClientType() string // persiaos, web, android, ios, ...
	// Geo()                // location of user or post

	protocol.Storage_SaveTime // Request time or save Time of the request not the created record by this record.
}
