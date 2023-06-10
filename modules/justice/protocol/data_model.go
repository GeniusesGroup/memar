/* For license and copyright information please see the LEGAL file in the code repository */

package org

/*
# Justice Service
Each org (police is org!) or person can fill a sue! Story is like an org own a road that a car driver do something against rules e.g. speed and org staff as road guard(police) can fill a sue in very easy way e.g. send a picture and sue fill automatically!!
Each claim just approve or decline not any text to describe how to run court decision!! Claim type is fixed!!

## Usage
- can block user balance and transfer it.
*/

// Case :
type Case struct {
	UserID    [16]byte
	OtherSide [16]byte
	ClaimType uint16 // We just accept specific claim type
}

// Claim types
const (
// Identity theft
//
)
