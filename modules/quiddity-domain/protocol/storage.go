/* For license and copyright information please see LEGAL file in repository */

package protocol

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// QuiddityDomain indicate the domain record data fields.
type QuiddityDomain interface {
	QuiddityID() [16]byte           // Unique content ID
	DomainID() protocol.MediaTypeID // Domain MediaTypeID e.g. product, content, ... domain
	Time() protocol.Time            // save time
	RequestID() [16]byte            // user-request domain
}

type StorageServices interface {
	Save(qd QuiddityDomain) (err protocol.Error)

	Get(quiddityID [16]byte) (qd QuiddityDomain, err protocol.Error)
}
