/* For license and copyright information please see the LEGAL file in the code repository */

package user_p

import (
	record_p "memar/storage/record/protocol"
)

type Field_UserUUID interface {
	UserID() UUID
}

// Generated unique ID for the user
type UUID record_p.UUID

// Register new user
