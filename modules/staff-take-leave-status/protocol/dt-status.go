/* For license and copyright information please see the LEGAL file in the code repository */

package stlsp

import (
	qsp "org/modules/quiddity-status/protocol"
)

type Status qsp.Quiddity_Status

const (
	Status_NeedAlternate = Status(qsp.Quiddity_Status_FreeFlag << iota)
	Status_NeedAlternateApprove
	Status_AlternateApprove
	Status_NeedManagerApprove
	Status_ManagerApprove
)
