/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// UserReferent indicate the domain record data fields.
type UserReferent interface {
	UserID() up.UserUUID            //
	ReferentUserID() up.UserUUID    //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type UserReferent_StorageServices interface {
	Save(ur UserReferent) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(userID up.UserUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(userID up.UserUUID, vo protocol.VersionOffset) (ur UserReferent, nv protocol.NumberOfVersion, err protocol.Error)

	FindByReferentUserID(referentUserID up.UserUUID, offset, limit uint64) (userIDs []up.UserUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
