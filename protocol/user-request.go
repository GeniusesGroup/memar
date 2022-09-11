/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

type UserRequestUUID = protocol.UUID

// UserRequest use to prove how other records created as a chain to other records or standalone data.
type UserRequest interface {
	RequestID() UserRequestUUID     //
	DomainID() uint64               // Domain MediaTypeID e.g. product, content, ... domain
	PastRequestID() UserRequestUUID // user-request domain. to chain related requests that create||update the same record.
	UserID() protocol.UserID        // user domain
	UserConnectionID() [16]byte     // Store to remember request belong to which Connection/AppInstance.
	// ClientType() string // persiaos, web, android, ios, ...
	Geo()                // location of user or post
	ServiceID() uint64   //
	CompressID() uint64  // gzip, ...
	Request() []byte     // Decode by service request structure and compress type.
	Time() protocol.Time // Request time or save Time of the request not the created record by this record.
	Signature() []byte   // Store to prove user requested to set||update this record.
}

type UserRequest_StorageServices interface {
	Save(q UserRequest) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(requestID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(requestID [16]byte, vo protocol.VersionOffset) (ur UserRequest, nv protocol.NumberOfVersion, err protocol.Error)

	FindByDomain(domainID uint64, offset, limit uint64) (requestIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
	FindByUser(userID [16]byte, offset, limit uint64) (requestIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}
