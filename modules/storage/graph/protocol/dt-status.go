/* For license and copyright information please see the LEGAL file in the code repository */

package qrq_p

import (
	qs_p "org/modules/identity/quiddity-status/protocol"
)

type Field_Status interface {
	Status() Status
}

type Status qs_p.Quiddity_Status

const (
	Status_Optional = Status(qs_p.Quiddity_Status_FreeFlag << iota)
)
