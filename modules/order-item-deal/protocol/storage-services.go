/* For license and copyright information please see the LEGAL file in the code repository */

package oidp

import (
	"libgo/protocol"

	op "org/modules/order/protocol"
	up "org/modules/user/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Get(orderID op.OrderUUID) (dm DataModel, err protocol.Error)

	FindByUserID(userID up.UserUUID, offset, limit uint64) (orderIDs []op.OrderUUID, nv protocol.NumberOfVersion, err protocol.Error)
	FindByKindID(kindID [16]byte, offset, limit uint64) (orderIDs []op.OrderUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
