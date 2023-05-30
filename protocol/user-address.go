/* For license and copyright information please see the LEGAL file in the code repository */

package org

import urp "org/modules/user-request/protocol"

type UserAddress interface {
	UserID() UserUUID //
	// TODO:::
	Address() string
	Status() UserAddressStatus
	RequestID() urp.UserRequestUUID //
}

type UserAddressStatus Quiddity_Status
