/* For license and copyright information please see the LEGAL file in the code repository */

package cts

import (
	qsp "org/modules/quiddity-status/protocol"
)

type Status qsp.Quiddity_Status

const (
	Status_Draft = Status(qsp.Quiddity_Status_FreeFlag << iota)
)
