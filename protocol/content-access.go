/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type ContentAccess interface {
	ContentID() ContentUUID         //
	Access() Content_Access         //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type ContentAccess_StorageServices interface {
	Save(ca ContentAccess) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(contentID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(contentID [16]byte, vo protocol.VersionOffset) (ca ContentAccess, nv protocol.NumberOfVersion, err protocol.Error)
}

type Content_Access uint8

const (
	Content_Access_Unset    Content_Access = 0
	Content_Access_UserList Content_Access = (1 << iota)
	Content_Access_Public
	Content_Access_RegisteredUser
	Content_Access_PremiumUser // usually charge for monthly access.  /// other plan?? basic, ... /// role based??
)
