/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// QuiddityComplement indicate the domain record data fields.
type QuiddityComplement interface {
	QuiddityID() QuiddityUUID       //
	Priority() uint64               // Complement priority
	ComplementID() QuiddityUUID     //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type QuiddityComplement_StorageServices interface {
	Save(pc QuiddityComplement) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(quiddityID QuiddityUUID, priority uint64) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(quiddityID QuiddityUUID, priority uint64, vo protocol.VersionOffset) (pc QuiddityComplement, nv protocol.NumberOfVersion, err protocol.Error)

	ListQuiddities(complementID QuiddityUUID, offset, limit uint64) (quiddityIDs []QuiddityUUID, nv protocol.NumberOfVersion, err protocol.Error)
	ListPriorities(complementID, quiddityID QuiddityUUID, offset, limit uint64) (priorities []uint64, nv protocol.NumberOfVersion, err protocol.Error)
}
