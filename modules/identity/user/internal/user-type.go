/* For license and copyright information please see the LEGAL file in the code repository */

package user

import (
	user_p "org/modules/identity/user/protocol"
)

// CheckUserType check and return error if user not exist in base users
func CheckUserType(baseUsers, user user_p.Type) (exist bool) {
	return user&baseUsers == user
	// err = &ErrUserNotAllow
}
