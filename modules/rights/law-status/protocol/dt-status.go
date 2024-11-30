/* For license and copyright information please see the LEGAL file in the code repository */

package lsp

import (
	qsp "org/modules/identity/quiddity-status/protocol"
)

type Field_Status interface {
	Status() Status
}

type Status qsp.Quiddity_Status

const (
	Status_Suggestion = Status(qsp.Quiddity_Status_FreeFlag << iota)
	Status_Closed
	Status_Approved
	Status_Denied
)
