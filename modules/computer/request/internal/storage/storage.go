/* For license and copyright information please see the LEGAL file in the code repository */

package ur

// Request use ObjectID of this record to prove how other object created as a chain to other object or standalone data.
type Request struct {
	UserID           [32]byte
	UserConnectionID [32]byte // Store to remember which ConnectionID/AppInstanceID set||chanaged this record.
	UserSignature    []byte   // Store to prove user requested to set||update this record.
	ServiceID        uint64
	Request          []byte
}

// UserRequest ---Read locale description in UserRequestStructure---
type UserRequest []byte

// func (ur UserRequest) UserConnectionID() (appInsID [32]byte) { copy(appInsID[:], ur[0:]); return }
// func (ur UserRequest) UserSignature() (connID [32]byte)      { copy(connID[:], ur[32:]); return }
// func (ur UserRequest) ServiceID() (connID [32]byte)          { copy(connID[:], ur[32:]); return }
// func (ur UserRequest) Request() (connID [32]byte)            { copy(connID[:], ur[32:]); return }
