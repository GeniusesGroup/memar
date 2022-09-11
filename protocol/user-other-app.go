/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// UserOtherApp store data about user delegation to this org(app) in other orgs(apps)
type UserOtherApp interface {
	UserID() protocol.UserID    // user domain
	OrgID() protocol.UserID     // user domain
	Domain() string             // unique name in the computer world. Country e.g. Iran, ... || Digital platforms e.g. Instagram, Facebook, Google, Github, Yahoo, ...
	DomainUserID() []byte       // user id in that domain e.g. country national code
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type UserOtherApp_StorageServices interface {
	Save(uoa UserOtherApp) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(userID, orgID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(userID, orgID [16]byte, vo protocol.VersionOffset) (uoa UserOtherApp, nv protocol.NumberOfVersion, err protocol.Error)

	FindByDomainUserID(domainUserID string, offset, limit uint64) (userIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)

	ListOrgs(userID [16]byte, offset, limit uint64) (orgIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}
