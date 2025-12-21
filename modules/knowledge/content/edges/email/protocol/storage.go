/* For license and copyright information please see the LEGAL file in the code repository */

package email_p

import (
	error_p "memar/error/protocol"

	cp "org/modules/knowledge/comment/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv storage_p.NumberOfVersion, err error_p.Error)

	Count(commentID cp.UUID) (nv storage_p.NumberOfVersion, err error_p.Error)
	Get(commentID cp.UUID, vo storage_p.VersionOffset) (dm DataModel, nv storage_p.NumberOfVersion, err error_p.Error)
}
