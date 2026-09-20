/* For license and copyright information please see the LEGAL file in the code repository */

package urp

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// UserRequest use to prove how other records created as a chain to other records or standalone data.
type Storage interface {
	RequestID() urp.UserRequestUUID //
	CompressID() uint64             // gzip, ...
	Request() []byte                // Decode by service request structure and compress type.
	Signature() []byte              // Store to prove user requested to set||update this record.
}

type StorageServices interface {
	Save(q Storage) (err protocol.Error)

	Get(requestID urp.UserRequestUUID) (ur Storage, err protocol.Error)

	Delete(requestID urp.UserRequestUUID) (err protocol.Error)
}
