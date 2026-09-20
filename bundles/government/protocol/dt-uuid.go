/* For license and copyright information please see the LEGAL file in the code repository */

package government_p

import (
	user_p "org/modules/identity/user/protocol"
)

type Field_GovernmentID interface {
	GovernmentID() user_p.UUID
}
