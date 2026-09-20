/* For license and copyright information please see the LEGAL file in the code repository */

package password_p

import (
	user_p "org/modules/identity/user/protocol"
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
		PersonID() user_p.UUID
		PasswordHash() []byte
	}
	BS_Confirm_Response interface {
		// Token() []byte
		// Status() Status
	}
)
