/* For license and copyright information please see the LEGAL file in the code repository */

package rp

// Status indicate Reaction record status
type Status uint8

// Reaction status
const (
	Status_Unset  Status = 0
	Status_Hidden Status = (1 << iota) // to indicate just peer can access the interest chains.
	Status_Blocked
)
