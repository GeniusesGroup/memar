/* For license and copyright information please see the LEGAL file in the code repository */

package uap

import (
	qsp "org/modules/quiddity-status/protocol"
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

type DataModel interface {
	UserID() up.UserUUID //
	// TODO:::
	Address() string
	Status() Status
	RequestID() urp.UserRequestUUID //
}

type Status qsp.Quiddity_Status
