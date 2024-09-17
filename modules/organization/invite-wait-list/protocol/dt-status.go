/* For license and copyright information please see the LEGAL file in the code repository */

package iwlp

type Status uint8

const (
	Status_Unset     Status = iota
	Status_Wait             // GUI base
	Status_Confirmed        //
	Status_Canceled         //
	Status_Expired          // GUI base
)
