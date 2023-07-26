/* For license and copyright information please see the LEGAL file in the code repository */

package psp

import (
	qsp "org/modules/quiddity-status/protocol"
)

type Status qsp.Quiddity_Status

const (
	Pos_Status_CashLimitInactivated = Status(qsp.Quiddity_Status_FreeFlag << iota)
)
