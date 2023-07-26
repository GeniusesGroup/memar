/* For license and copyright information please see the LEGAL file in the code repository */

package iip

type Status uint8

const (
	Status_Unset    Status = 0
	Status_DoNotAdd Status = (1 << iota)
	Status_SoftDelete
	Status_Extra
)
