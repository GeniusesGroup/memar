/* For license and copyright information please see the LEGAL file in the code repository */

package cop

import (
	error_p "memar/process/error/protocol"

	storage_p "memar/storage/protocol"
	cp "org/modules/knowledge/content/edges-loop/comment/protocol"
	op "org/modules/storage/object/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (err error_p.Error)

	Get(commentID cp.UUID, vo storage_p.VersionOffset) (dm DataModel, err error_p.Error)

	FIND_CommentIDs_BY_ObjectID(objectID op.UUID, offset, limit uint64) (commentIDs []cp.UUID, num storage_p.NumberOfVersion, err error_p.Error)
}
