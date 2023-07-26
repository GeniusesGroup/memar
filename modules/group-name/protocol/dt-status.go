/* For license and copyright information please see the LEGAL file in the code repository */

package gnp

// Status indicate GroupName record status
type Status uint8

// GroupName status
const (
	Status_Unset    Status = 0
	Status_Register Status = (1 << iota)
	Status_Remove
	Status_Blocked
	Status_Reserved
)
