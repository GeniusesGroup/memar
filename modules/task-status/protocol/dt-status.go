/* For license and copyright information please see the LEGAL file in the code repository */

package tsp

import (
	qsp "org/modules/quiddity-status/protocol"
)

type Status qsp.Quiddity_Status

const (
	Status_ReadyForDevelopment = Status(qsp.Quiddity_Status_FreeFlag << iota)
	Status_InProgress
	Status_Close
	Status_Success
)
