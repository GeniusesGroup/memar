/* For license and copyright information please see the LEGAL file in the code repository */

package qu_p

import (
	error_p "memar/process/error/protocol"

	storage_p "memar/storage/protocol"
	qp "org/modules/identity/thing/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (err error_p.Error)

	Get(uri URI) (dm DataModel, err error_p.Error)

	FindByQuiddity(quiddityID qp.UUID, offset, limit uint64) (uris []URI, nv storage_p.NumberOfVersion, err error_p.Error)
}
