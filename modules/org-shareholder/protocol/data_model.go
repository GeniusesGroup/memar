/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

type OrgShareholder interface {
	OrgID() OrgUUID
	UserID() up.UserUUID            //
	Quantity() protocol.PerTrillion //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type OrgShareholder_StorageServices interface {
	Save(dm OrgShareholder) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(orgID OrgUUID, userID up.UserUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(orgID OrgUUID, userID up.UserUUID, vo protocol.VersionOffset) (dm OrgShareholder, err protocol.Error)

	LIST_UserIDs_BY_OrgID(orgID OrgUUID, offset, limit uint64) (userIDs []up.UserUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
