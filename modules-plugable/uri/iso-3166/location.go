/* For license and copyright information please see the LEGAL file in the code repository */

package ar_p

// https://en.wikipedia.org/wiki/ISO_3166
type Location struct {
	Alpha2 [2]byte // 2 english alphabet
	Alpha3 [3]byte // 3 english alphabet
	Num    [3]byte // 3 digit
	Name   string
	// Currencies []*Currency
}
