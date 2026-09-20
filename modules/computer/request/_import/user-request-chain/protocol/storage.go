/* For license and copyright information please see the LEGAL file in the code repository */

package urp

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// UserRequest use to prove how other records created as a chain to other records or standalone data.
type Storage interface {
	RequestID() urp.UserRequestUUID     //
	PastRequestID() urp.UserRequestUUID // user-request domain. to chain related requests that create||update the same record.
}

type StorageServices interface {
	Save(s Storage) (err protocol.Error)

	Get(requestID urp.UserRequestUUID) (s Storage, err protocol.Error)
}
