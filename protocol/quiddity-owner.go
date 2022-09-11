/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// QuiddityOwner indicate the domain record data fields.
type QuiddityOwner interface {
	QuiddityID() [16]byte       // Unique content ID
	UserID() protocol.UserID    // user domain. Owner of the quiddity
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type QuiddityOwner_StorageServices interface {
	Save(qo QuiddityOwner) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(quiddityID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(quiddityID [16]byte, vo protocol.VersionOffset) (qo QuiddityOwner, nv protocol.NumberOfVersion, err protocol.Error)

	FindByOwnerID(userID [16]byte, offset, limit uint64) (quiddityIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}

type QuiddityOwner_Service_FindByUserID_Request interface {
	UserID() [32]byte
	Offset() uint64
	Limit() uint64
}
type QuiddityOwner_Service_FindByUserID_Response interface {
	QuiddityIDs() [][32]byte
	Numbers() uint64
}
