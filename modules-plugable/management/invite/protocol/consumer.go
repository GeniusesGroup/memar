/* For license and copyright information please see the LEGAL file in the code repository */

package ig_p

import (
	user_p "org/modules/identity/user/protocol"
)

type Usable interface {
	PermitUsageIDs() []user_p.UUID
}
