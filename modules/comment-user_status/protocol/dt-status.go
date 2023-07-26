/* For license and copyright information please see the LEGAL file in the code repository */

package cus

type Status uint8

const (
	Status_Unset Status = iota
	Status_Delivered
	Status_Seen
	Status_Read
)
