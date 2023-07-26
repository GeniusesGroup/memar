/* For license and copyright information please see the LEGAL file in the code repository */

package csp

import (
	"memar/protocol"

	cp "org/modules/comment/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(commentID cp.CommentUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(commentID cp.CommentUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)
}
