/* For license and copyright information please see the LEGAL file in the code repository */

package discount

import (
	user_p "org/modules/identity/user/protocol"
)

type User interface {
	user_p.Field_UserUUID
}
