/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// UserOtherApp store data about user delegation to this org(app) in other orgs(apps)
type UserOtherApp interface {
	UserID() up.UserUUID               //
	OrgID() up.UserUUID                //
	DomainUserID() up.UserUUID         // user id in that domain e.g. country national code
	OurGeneratedUserUUID() up.UserUUID // it will generate to fix same UUID collision problem
	Time() protocol.Time               // save time
	RequestID() urp.UserRequestUUID    //
}

type UserOtherApp_StorageServices interface {
	Save(uoa UserOtherApp) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(userID, orgID up.UserUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(userID, orgID up.UserUUID, vo protocol.VersionOffset) (uoa UserOtherApp, nv protocol.NumberOfVersion, err protocol.Error)

	FindByDomainUserID(domainUserID up.UserUUID, offset, limit uint64) (userIDs []UserOtherApp, nv protocol.NumberOfVersion, err protocol.Error)
	FindByDomainUserIDOrgID(domainUserID up.UserUUID, orgID up.UserUUID, offset, limit uint64) (userIDs []up.UserUUID, nv protocol.NumberOfVersion, err protocol.Error)

	ListUsers(orgID up.UserUUID, offset, limit uint64) (userIDs []up.UserUUID, nv protocol.NumberOfVersion, err protocol.Error)
	ListOrgs(userID up.UserUUID, offset, limit uint64) (orgIDs []up.UserUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
