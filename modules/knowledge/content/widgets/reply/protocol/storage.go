/* For license and copyright information please see the LEGAL file in the code repository */

package crp

import (
	error_p "memar/process/error/protocol"

	storage_p "memar/storage/protocol"
	cp "org/modules/knowledge/content/edges-loop/comment/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (err error_p.Error)

	Get(commentID cp.UUID) (dm DataModel, err error_p.Error)

	FIND_CommentIDs_BY_ReplyToID(replyTo cp.UUID, offset, limit uint64) (commentIDs []cp.UUID, num storage_p.NumberOfVersion, err error_p.Error)
}
