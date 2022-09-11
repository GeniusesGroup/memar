/* For license and copyright information please see the LEGAL file in the code repository */

package org

// Production is the structure of production line.
// https://www.zenscale.in/planning
type Production interface {
	ID() [16]byte // quiddity domain.
	StartDate() uint64
	EndDate() uint64
	Number() uint64
	Status() uint8
}

//Created
//ManagerApprove
//WarehouseApprove
//ActiveWithApprove
//ActiveWithoutApprove
//ActiveWithOrderer
//Inactive
//Normal
//Reject
//Void
