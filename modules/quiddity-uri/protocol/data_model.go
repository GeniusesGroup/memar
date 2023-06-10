/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// QuiddityURI indicate the domain record data fields.
// https://en.wikipedia.org/wiki/Uniform_Resource_Identifier
// https://en.wikipedia.org/wiki/Uniform_Resource_Name
// https://en.wikipedia.org/wiki/Electronic_Product_Code
type QuiddityURI interface {
	URI() []byte                    // Locale name in the Computer world.
	QuiddityID() QuiddityUUID       //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type QuiddityURI_StorageServices interface {
	Save(q QuiddityURI) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(uri []byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(uri []byte, vo protocol.VersionOffset) (q QuiddityURI, nv protocol.NumberOfVersion, err protocol.Error)

	FindByQuiddity(quiddityID QuiddityUUID, offset, limit uint64) (uris [][]byte, nv protocol.NumberOfVersion, err protocol.Error)
}
