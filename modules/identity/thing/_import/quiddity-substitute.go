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

	// FIND_CategoryIDs_BY_SubstituteID(substituteID CategoryUUID, offset, limit uint64) (categoryIDs []CategoryUUID, nv protocol.NumberOfVersion, err protocol.Error)
	// LIST_SubstituteIDs_BY_CategoryID(categoryID CategoryUUID, offset, limit uint64) (substituteIDs []CategoryUUID, nv protocol.NumberOfVersion, err protocol.Error)
	// LIST_Priorities_BY_CategoryID(categoryID CategoryUUID, offset, limit uint64) (priorities []uint64, nv protocol.NumberOfVersion, err protocol.Error)
}
