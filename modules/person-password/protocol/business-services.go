/* For license and copyright information please see the LEGAL file in the code repository */

package ppp

import (
	up "org/modules/user/protocol"
)

type (
	BS_SendResetToken_Request interface {
		How() uint8 // sms, email, ...
	}
	BS_SendResetToken_Response interface {
		Token() []byte // include Token&ExpireIn with signature by domain key.
	}
)

type (
	BS_Register_Request interface {
		PasswordHash() []byte
	}
)
type (
	BS_Confirm_Request interface {
		PersonID() up.UserUUID
		PasswordHash() []byte
	}
	BS_Confirm_Response interface {
		// Token() []byte
		Status() Status
	}
)
