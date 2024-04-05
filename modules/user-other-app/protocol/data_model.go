/* For license and copyright information please see the LEGAL file in the code repository */

package uoap

import (
	"memar/protocol"

	aap "org/modules/app-audit/protocol"
	up "org/modules/user/protocol"
)

// DataModel store data about user delegation to this org(app) in other orgs(apps)
type DataModel interface {
	UserID() up.UserUUID
	OrgID() up.UserUUID
	DomainUserID() up.UserUUID         // user id in that domain e.g. country national code
	OurGeneratedUserUUID() up.UserUUID // it will generate to fix same UUID collision problem

	aap.AuditRequest
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
