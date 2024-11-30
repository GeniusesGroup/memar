/* For license and copyright information please see the LEGAL file in the code repository */

package lsp

import (
	error_p "memar/error/protocol"

	lp "org/modules/rights/law/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv storage_p.NumberOfVersion, err error_p.Error)

	Count(lawID lp.UUID) (nv storage_p.NumberOfVersion, err error_p.Error)
	Get(lawID lp.UUID, vo storage_p.VersionOffset) (dm DataModel, nv storage_p.NumberOfVersion, err error_p.Error)

	// FilterByStatus(status Status, offset, limit uint64) (lawIDs []lp.UUID, nv storage_p.NumberOfVersion, err error_p.Error)
}
