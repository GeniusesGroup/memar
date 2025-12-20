/* For license and copyright information please see the LEGAL file in the code repository */

package user_p

import (
	quiddity_p "org/modules/identity/quiddity/protocol"
)

type Field_UserID interface {
	UserID() UUID
}

// Generated unique ID for the user
type UUID quiddity_p.UUID

// Register new user
