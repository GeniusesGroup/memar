/* For license and copyright information please see the LEGAL file in the code repository */

package user_active

import (
	society_p "org/modules/identity/society/protocol"
	user_p "org/modules/identity/user/protocol"
)

// OperatingSystem_User introduce all data about an applications
type OperatingSystem_User interface {
	ActiveUser() User
	Users() []User
}

type User interface {
	ID() user_p.UUID
	SocietyID() society_p.UUID
}
