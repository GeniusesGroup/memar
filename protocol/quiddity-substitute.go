/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// QuidditySubstitute indicate the domain record data fields.
// or similar product
type QuidditySubstitute interface {
	QuiddityID() QuiddityUUID       //
	Priority() uint64               // Substitute priority
	SubstituteID() QuiddityUUID     //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type QuidditySubstitute_StorageServices interface {
	Save(ps QuidditySubstitute) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(quiddityID QuiddityUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(quiddityID QuiddityUUID, vo protocol.VersionOffset) (ps QuidditySubstitute, nv protocol.NumberOfVersion, err protocol.Error)

	FindBySubstitute(substituteID QuiddityUUID, offset, limit uint64) (quiddityIDs []QuiddityUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
