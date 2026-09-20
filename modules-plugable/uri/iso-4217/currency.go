/* For license and copyright information please see the LEGAL file in the code repository */

package iso4217

// Currency indicate to store a currency with helpfull methods
// https://en.wikipedia.org/wiki/ISO_4217
type Currency struct {
	Code [3]byte // 3 english alphabet
	Num  [3]byte // 3 digit number code
	DS   int     // The number of digits after the decimal separator
	Name string
	// Locations []*Location
}
