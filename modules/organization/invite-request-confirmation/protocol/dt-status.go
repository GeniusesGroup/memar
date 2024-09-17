/* For license and copyright information please see the LEGAL file in the code repository */

package ircp

type Status uint8

const (
	Status_Unset    Status = iota
	Status_OnHold          // GUI base
	Status_Accepted        //
	Status_Rejected        //
	Status_Expired         // GUI base
)
