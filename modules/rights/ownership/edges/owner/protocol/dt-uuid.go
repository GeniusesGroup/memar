/* For license and copyright information please see the LEGAL file in the code repository */

package owner_p

import (
	user_p "org/modules/identity/user/protocol"
)

type Field_OwnerID interface {
	OwnerID() user_p.UUID
}
