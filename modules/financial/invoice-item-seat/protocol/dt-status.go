/* For license and copyright information please see the LEGAL file in the code repository */

package iisp

import (
	qsp "org/modules/identity/quiddity-status/protocol"
)

type Field_Status interface {
	Status() Status
}

type Status qsp.Quiddity_Status

const (
	Status_Voided = Status(qsp.Quiddity_Status_FreeFlag << iota)
)
