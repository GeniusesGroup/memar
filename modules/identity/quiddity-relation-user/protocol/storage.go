/* For license and copyright information please see the LEGAL file in the code repository */

package qru_p

import (
	error_p "memar/error/protocol"

	qp "org/modules/identity/quiddity/protocol"
	user_p "org/modules/identity/user/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (err error_p.Error)

	Get(quiddityID qp.UUID) (dm DataModel, err error_p.Error)

	FindByOwnerID(userID user_p.UUID, offset, limit uint64) (quiddityIDs []qp.UUID, nv storage_p.NumberOfVersion, err error_p.Error)
}
