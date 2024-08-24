/* For license and copyright information please see the LEGAL file in the code repository */

package osp

import (
	"memar/protocol"

	op "org/modules/order/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(orderID op.OrderUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(orderID op.OrderUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	// FilterByStatus(status Status, offset, limit uint64) (orderIDs []op.OrderUUID , nv protocol.NumberOfVersion, err protocol.Error)
}
