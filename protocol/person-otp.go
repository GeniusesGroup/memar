/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// PersonOTP indicate the domain record data fields.
type PersonOTP interface {
	PersonID() UserUUID             //
	OTPPattern() []byte             // https://tools.ietf.org/html/rfc6238
	OTPAdditional() int32           // easy to remember and must be 2 to 7 digit. https://en.wikipedia.org/wiki/Personal_identification_number
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type PersonOTP_StorageServices interface {
	Save(po PersonOTP) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(personID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(personID [16]byte, vo protocol.VersionOffset) (po PersonOTP, nv protocol.NumberOfVersion, err protocol.Error)
}
