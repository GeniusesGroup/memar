/* For license and copyright information please see the LEGAL file in the code repository */

package uoap

import (
	"libgo/protocol"

	up "org/modules/user/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(userID, orgID up.UserUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(userID, orgID up.UserUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FindByDomainUserID(domainUserID up.UserUUID, offset, limit uint64) (userIDs []DataModel, nv protocol.NumberOfVersion, err protocol.Error)
	FindByDomainUserIDOrgID(domainUserID up.UserUUID, orgID up.UserUUID, offset, limit uint64) (userIDs []up.UserUUID, nv protocol.NumberOfVersion, err protocol.Error)

	ListUsers(orgID up.UserUUID, offset, limit uint64) (userIDs []up.UserUUID, nv protocol.NumberOfVersion, err protocol.Error)
	ListOrgs(userID up.UserUUID, offset, limit uint64) (orgIDs []up.UserUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
