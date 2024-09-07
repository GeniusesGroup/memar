/* For license and copyright information please see the LEGAL file in the code repository */

package bp_p

import (
	ut16 "memar/identifier/uuid-time-16byte"
)

type Field_BusinessPageID interface {
	BusinessPageID() PageUUID
}

type PageUUID ut16.UUID
