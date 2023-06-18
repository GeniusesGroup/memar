/* For license and copyright information please see the LEGAL file in the code repository */

package cap

import (
	"libgo/protocol"

	cp "org/modules/content/protocol"
	urp "org/modules/user-request/protocol"
)

type DataModel interface {
	ContentID() cp.ContentUUID      //
	Access() Content_Access         //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}



type Content_Access uint8

const (
	Content_Access_Unset    Content_Access = 0
	Content_Access_UserList Content_Access = (1 << iota)
	Content_Access_Public
	Content_Access_RegisteredUser
	Content_Access_PremiumUser // usually charge for monthly access.  /// other plan?? basic, ... /// role based??
)
