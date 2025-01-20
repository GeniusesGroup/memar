/* For license and copyright information please see the LEGAL file in the code repository */

package quiddity_p

import (
	storage_p "org/modules/storage/primitive/protocol"
)

type Field_QuiddityID interface {
	// Quiddity is the essence that makes something the kind of thing it is and makes it different from any other
	QuiddityID() UUID
}

// UUID can be same with any other UUID domains e.g. user, ...
// It MUST be unique ID in all domains.
// Usually use to SET/GET and show locale title by knowledge/text domain.
type UUID storage_p.RecordUUID
