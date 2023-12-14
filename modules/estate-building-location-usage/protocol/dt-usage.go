/* For license and copyright information please see the LEGAL file in the code repository */

package eblup

// property use
type Usage uint16

const (
	Usage_Unset Usage = iota
	Usage_Residential
	Usage_Commercial
	Usage_Storage
)
