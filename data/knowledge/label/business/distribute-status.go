/* For license and copyright information please see the LEGAL file in the code repository */

package label

// DC abbreviation for distribution-center or Warehouse
const (
	Status_OutcomeDCRequested =  iota
	Status_IncomeDCRequested
	Status_OutcomeDCApproved
	Status_IncomeDCApproved
	Status_Void
)
