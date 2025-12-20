/* For license and copyright information please see the LEGAL file in the code repository */

package user_p

import (
	time_p "memar/time/protocol"
)

type ID interface {
	UUID() UUID

	// Below fields extract from(part of) above UUID
	ExistenceTime() time_p.Time
	Field_UserType
	ID() [3]byte
}
