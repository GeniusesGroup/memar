/* For license and copyright information please see the LEGAL file in the code repository */

package voucher

import (
	m_user_p "memar/user/protocol"

	user_p "org/modules/identity/user/protocol"
)

// Use to restrict the voucher usage by specific users.
type User_ID interface {
	user_p.Field_UserID
}

// Use to restrict the voucher usage by specific user type.
type User_Type interface {
	m_user_p.Field_UserType
}
