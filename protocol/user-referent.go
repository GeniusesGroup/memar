/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// UserReferent indicate the domain record data fields.
type UserReferent interface {
	UserID() UserUUID               //
	ReferentUserID() UserUUID       //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type UserReferent_StorageServices interface {
	Save(ur UserReferent) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(userID UserUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(userID UserUUID, vo protocol.VersionOffset) (ur UserReferent, nv protocol.NumberOfVersion, err protocol.Error)

	FindByReferentUserID(referentUserID UserUUID, offset, limit uint64) (userIDs []UserUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
