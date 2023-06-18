/* For license and copyright information please see the LEGAL file in the code repository */

package lsp

import (
	"libgo/protocol"

	lp "org/modules/law/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(lawID lp.LawUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(lawID lp.LawUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	// FilterByStatus(status Status, offset, limit uint64) (lawIDs []lp.LawUUID, nv protocol.NumberOfVersion, err protocol.Error)

	// protocol.EventTarget
}
