/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// UserReferent indicate the domain record data fields.
type UserReferent interface {
	UserID() protocol.UserID         // user domain
	ReferentUserID() protocol.UserID // user domain
	Time() protocol.Time             // save time
	RequestID() UserRequestUUID      // user-request domain
}

type UserReferent_StorageServices interface {
	Save(ur UserReferent) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(userID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(userID [16]byte, vo protocol.VersionOffset) (ur UserReferent, nv protocol.NumberOfVersion, err protocol.Error)

	FindByReferentUserID(referentUserID [16]byte, offset, limit uint64) (userIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}
