/* For license and copyright information please see the LEGAL file in the code repository */

package bm_p

import (
	ut16 "memar/identifier/uuid-time-16byte"
)

type Field_ModuleID interface {
	BusinessModuleID() ModuleUUID
}

// Applications module identifier e.g. product, content, ... domain
type ModuleUUID ut16.UUID
