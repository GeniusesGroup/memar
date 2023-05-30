/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// UserOtherApp store data about user delegation to this org(app) in other orgs(apps)
type UserOtherApp interface {
	UserID() UserUUID               //
	OrgID() UserUUID                //
	DomainUserID() UserUUID         // user id in that domain e.g. country national code
	OurGeneratedUserUUID() UserUUID // it will generate to fix same UUID collision problem
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type UserOtherApp_StorageServices interface {
	Save(uoa UserOtherApp) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(userID, orgID UserUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(userID, orgID UserUUID, vo protocol.VersionOffset) (uoa UserOtherApp, nv protocol.NumberOfVersion, err protocol.Error)

	FindByDomainUserID(domainUserID UserUUID, offset, limit uint64) (userIDs []UserOtherApp, nv protocol.NumberOfVersion, err protocol.Error)
	FindByDomainUserIDOrgID(domainUserID UserUUID, orgID UserUUID, offset, limit uint64) (userIDs []UserUUID, nv protocol.NumberOfVersion, err protocol.Error)

	ListUsers(orgID UserUUID, offset, limit uint64) (userIDs []UserUUID, nv protocol.NumberOfVersion, err protocol.Error)
	ListOrgs(userID UserUUID, offset, limit uint64) (orgIDs []UserUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
