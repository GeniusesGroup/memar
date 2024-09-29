/* For license and copyright information please see the LEGAL file in the code repository */

package ls_p

import (
	error_p "memar/error/protocol"

	label_p "org/modules/knowledge/label/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv storage_p.NumberOfVersion, err error_p.Error)

	Get(lID label_p.UUID) (dm DataModel, err error_p.Error)

	FILTER_LabelIDs_BY_Status(status Status, offset, limit uint64) (lIDs []label_p.UUID, nv storage_p.NumberOfVersion, err error_p.Error)
}
