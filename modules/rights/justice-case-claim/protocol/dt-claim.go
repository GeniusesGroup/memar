/* For license and copyright information please see the LEGAL file in the code repository */

package jcc_p

type Field_Claim interface {
	Claim() Claim
}

// Claim types
// Just accept specific claim type
type Claim uint8

const (
	Claim_Unset Claim = iota

	// Identity theft
)
