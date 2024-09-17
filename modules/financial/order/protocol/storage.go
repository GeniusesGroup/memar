/* For license and copyright information please see the LEGAL file in the code repository */

package op

import (
	"memar/protocol"

	up "org/modules/user/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Get(orderID OrderUUID) (dm DataModel, err protocol.Error)

	FindByUserID(userID up.UserUUID, offset, limit uint64) (orderIDs []OrderUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
