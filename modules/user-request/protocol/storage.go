/* For license and copyright information please see the LEGAL file in the code repository */

package urp

import (
	"libgo/protocol"
)

// Storage_Fields indicates the domain record data fields.
type Storage_Fields interface {
	RequestID() UserRequestUUID //
	DomainID() uint64           // Domain MediaTypeID e.g. product, content, ... domain
	ServiceID() uint64          //
	UserID() protocol.UserID    // user domain
	UserConnectionID() [16]byte // Store to remember which request belongs to which Connection/AppInstance.
	// TODO::: move to esteghrar repo/connection
	// ClientType() string // persiaos, web, android, ios, ...
	// Geo()                // location of user or post
	Time() protocol.Time // Request time or save Time of the request not the created record by this record.
}

// Storage_Services indicates the domain storage layer services.
type Storage_Services interface {
	Save(sf Storage_Fields) (err protocol.Error)

	Get(requestID UserRequestUUID, vo protocol.VersionOffset) (sf Storage_Fields, err protocol.Error)

	FindByDomain(domainID uint64, offset, limit uint64) (requestIDs []UserRequestUUID, err protocol.Error)
	FindByUser(userID [16]byte, offset, limit uint64) (requestIDs []UserRequestUUID, err protocol.Error)
}
