/* For license and copyright information please see the LEGAL file in the code repository */

package upkp

// Status use to indicate UserPublicKey record status
type Status uint8

// UserPublicKey status
const (
	Status_Unset Status = iota
	Status_Active
	Status_Inactive
	Status_Blocked
	Status_Revoked
)
