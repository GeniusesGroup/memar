/* For license and copyright information please see the LEGAL file in the code repository */

package ar_p

type Status uint8

const (
	Answer_Unset Status = iota
	Answer_Passed
	Answer_Failed
)
