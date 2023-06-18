/* For license and copyright information please see the LEGAL file in the code repository */

package csp

import (
	"libgo/protocol"

	cp "org/modules/content/protocol"
	qsp "org/modules/quiddity-status/protocol"
	urp "org/modules/user-request/protocol"
)


type StorageServices interface {
	Save(f DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(contentID cp.ContentUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(contentID cp.ContentUUID, vo protocol.VersionOffset) (f DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FILTER_ContentIDs_BY_Status(status Content_Status, offset, limit uint64) (contentIDs []cp.ContentUUID, nv protocol.NumberOfVersion, err protocol.Error)

	// protocol.EventTarget
}
