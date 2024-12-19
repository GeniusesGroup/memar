/* For license and copyright information please see the LEGAL file in the code repository */

package ts_p

import (
	qs_p "org/modules/identity/quiddity-status/protocol"
)

const (
	Status_ReadyForDevelopment = qs_p.Status_FreeFlag << iota
	Status_InProgress
	Status_Close
	Status_Success
)
