/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// ProductUser indicate the domain record data fields.
type ProductUser interface {
	SubscriptionID() ProductUUID    //
	UserID() up.UserUUID            //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type ProductUser_StorageServices interface {
	Save(dm ProductUser) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID ProductUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID ProductUUID, vo protocol.VersionOffset) (dm ProductUser, nv protocol.NumberOfVersion, err protocol.Error)

}
