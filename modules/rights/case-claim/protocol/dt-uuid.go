/* For license and copyright information please see the LEGAL file in the code repository */

package jcc_p

type Field_ClaimNumber interface {
	ClaimNumber() ClaimNumber
}

// a comprehensive term for any proceeding in a court of law whereby an individual seeks a legal remedy
type ClaimNumber uint8
