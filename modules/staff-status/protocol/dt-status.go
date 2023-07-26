/* For license and copyright information please see the LEGAL file in the code repository */

package ssp

import (
	qsp "org/modules/quiddity-status/protocol"
)

type Status qsp.Quiddity_Status

const (
	Status_Hire = Status(qsp.Quiddity_Status_FreeFlag << iota)
	Status_Fire
	Status_End // death, end of contract, ...
	// Status_Active   // Shift
	// Status_Inactive // Shift
)
