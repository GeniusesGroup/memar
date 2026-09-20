/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// GroupUserAccessControl indicate the domain record data fields.
type GroupUserAccessControl interface {
	GroupID() [16]byte                     // group domain
	UserID() [16]byte                      //
	AccessControl() protocol.AccessControl //
	Time() protocol.Time                   // Save time
	RequestID() UserRequestUUID            // user-request domain
}

type UserRole_StorageServices interface {
	Save(ur UserRole) (numbers uint64, err protocol.Error)

	Count(id [16]byte) (numbers uint64, err protocol.Error)
	Get(id [16]byte, versionOffset uint64) (ur UserRole, err protocol.Error)
	Last(id [16]byte) (ur UserRole, err protocol.Error)

	GetIDs(offset, limit uint64) (ids [][16]byte, numbers uint64, err protocol.Error)
	// GetIDsByDateTime(time protocol.Time, offset, limit uint64) (ids [][16]byte, numbers uint64, err protocol.Error)
}
