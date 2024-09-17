/* For license and copyright information please see the LEGAL file in the code repository */

package acsp

import (
	qsp "org/modules/quiddity-status/protocol"
)

type Status qsp.Quiddity_Status

const (
	Status_New          = Status(qsp.Quiddity_Status_FreeFlag << iota) // means socket session not saved yet to storage
	Status_Loaded                                                      // means socket session load from storage
	Status_Unregistered                                                //
)
