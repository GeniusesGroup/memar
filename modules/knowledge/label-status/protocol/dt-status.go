/* For license and copyright information please see the LEGAL file in the code repository */

package ls_p

import (
	qsp "org/modules/identity/quiddity-status/protocol"
)

type Field_Status interface {
	LabelStatus() Status
}

type Status qsp.Quiddity_Status

const (
// Status_ = Status(Quiddity_Status_FreeFlag << iota)
)
