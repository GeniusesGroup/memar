/* For license and copyright information please see the LEGAL file in the code repository */

package csp

import (
	qsp "org/modules/quiddity-status/protocol"
)

type Status qsp.Quiddity_Status

const (
	Status_Negotiation = Status(qsp.Quiddity_Status_FreeFlag << iota)
	Status_PartlySigned
	Status_Signed
	Status_LegalAction
	Status_Done
	Status_Canceled
)
