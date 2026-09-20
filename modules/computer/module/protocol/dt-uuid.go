/* For license and copyright information please see the LEGAL file in the code repository */

package module_p

import (
	record_p "memar/storage/record/protocol"
)

type Field_ModuleUUID interface {
	ModuleUUID() UUID
	// DomainID() UUID
}

// Applications module identifier e.g. product, content, ... domain
type UUID record_p.UUID
