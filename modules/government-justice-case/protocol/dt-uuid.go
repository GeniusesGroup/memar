/* For license and copyright information please see the LEGAL file in the code repository */

package jc_p

import (
	ut16 "memar/identifier/uuid-time-16byte"
)

type Field_JusticeCaseID interface {
	JusticeCaseID() CaseUUID
}

// a comprehensive term for any proceeding in a court of law whereby an individual seeks a legal remedy
type CaseUUID ut16.UUID
