/* For license and copyright information please see the LEGAL file in the code repository */

package uoatp

import (
	"libgo/protocol"

	org "org/modules/org/protocol"
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

type DataModel interface {
	UserID() up.UserUUID            //
	OrgID() org.OrgUUID             //
	Token() []byte                  // DelegateToken, AccessToken
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
