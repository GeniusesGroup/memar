/* For license and copyright information please see the LEGAL file in the code repository */

package qmcp

import (
	error_p "memar/process/error/protocol"

	storage_p "memar/storage/protocol"
	qop "org/modules/knowledge/question_option/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv storage_p.NumberOfVersion, err error_p.Error)

	Count(questionOptionID qop.UUID) (nv storage_p.NumberOfVersion, err error_p.Error)
	Get(questionOptionID qop.UUID, vo storage_p.VersionOffset) (dm DataModel, nv storage_p.NumberOfVersion, err error_p.Error)
}
