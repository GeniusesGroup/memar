/* For license and copyright information please see the LEGAL file in the code repository */

package pjop

type Status uint8

const (
	Status_Unset Status = iota
	Status_Rework
	Status_Rejection
	Status_Approved
)
