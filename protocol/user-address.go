/* For license and copyright information please see the LEGAL file in the code repository */

package org

type UserAddress interface {
	UserID() [16]byte // UUID of User
	// TODO:::
	MobileNumber() string
	Status() UserAddressStatus
	RequestID() UserRequestUUID // user-request domain
}

type UserAddressStatus Quiddity_Status
