/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

type UserOtherAppToken interface {
	UserID() up.UserUUID            //
	OrgID() OrgUUID                 //
	Token() []byte                  // DelegateToken, AccessToken
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}
