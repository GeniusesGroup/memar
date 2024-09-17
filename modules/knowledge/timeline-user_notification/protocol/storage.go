/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"memar/protocol"

	up "org/modules/user/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Get(userID up.UserUUID) (dm DataModel, err protocol.Error)
}
