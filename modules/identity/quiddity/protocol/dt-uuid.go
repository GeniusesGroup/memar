/* For license and copyright information please see the LEGAL file in the code repository */

package quiddity_p

import (
	record_p "memar/storage/record/protocol"
)

type Field_QuiddityID interface {
	// Quiddity is the essence that makes something the kind of thing it is and makes it different from any other
	QuiddityID() UUID
}

type Field_QuidditiesID interface {
	// Quiddity is the essence that makes something the kind of thing it is and makes it different from any other
	QuidditiesID() []UUID
}

// UUID can be same with any other UUID domains e.g. user, ...
// It MUST be unique ID in all domains.
// Usually use to SET/GET and show locale title by knowledge/text domain.
type UUID record_p.UUID
