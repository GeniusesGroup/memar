/* For license and copyright information please see the LEGAL file in the code repository */

package crup

import (
	"memar/protocol"

	cp "org/modules/content/protocol"
	up "org/modules/user/protocol"
)

// TODO::: immutable?? if wrong data save for a content??
type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(contentID cp.ContentUUID, userID up.UserUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(contentID cp.ContentUUID, userID up.UserUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_ContentIDs_BY_UserID(userID up.UserUUID, offset, limit uint64) (contentIDs []cp.ContentUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_UserIDs_BY_ContentID(contentID cp.ContentUUID, offset, limit uint64) (userIDs []up.UserUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
