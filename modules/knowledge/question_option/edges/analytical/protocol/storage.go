/* For license and copyright information please see the LEGAL file in the code repository */

package qoa_p

import (
	error_p "memar/process/error/protocol"

	storage_p "memar/storage/protocol"
	question_p "org/modules/knowledge/question/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv storage_p.NumberOfVersion, err error_p.Error)

	Count(questionID question_p.UUID) (nv storage_p.NumberOfVersion, err error_p.Error)
	Get(questionID question_p.UUID, vo storage_p.VersionOffset) (dm DataModel, nv storage_p.NumberOfVersion, err error_p.Error)
}
