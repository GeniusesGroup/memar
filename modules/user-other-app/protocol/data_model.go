/* For license and copyright information please see the LEGAL file in the code repository */

package uoap

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// DataModel store data about user delegation to this org(app) in other orgs(apps)
type DataModel interface {
	UserID() up.UserUUID               //
	OrgID() up.UserUUID                //
	DomainUserID() up.UserUUID         // user id in that domain e.g. country national code
	OurGeneratedUserUUID() up.UserUUID // it will generate to fix same UUID collision problem
	SaveTime() protocol.Time           //
	RequestID() urp.UserRequestUUID    //
}

