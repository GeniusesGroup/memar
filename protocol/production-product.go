/* For license and copyright information please see the LEGAL file in the code repository */

package org

// Production is the structure of production line.
type ProductionProduct interface {
	ProductionID() [16]byte // production domain
	ProductID() [16]byte
	Number() uint64
	Status() uint8
}

// 0//created 1//ManagerApprove 2//WarehouseApprove 3//ActiveWithApprove 4//ActiveWithoutApprove 5//ActiveWithOrderer 6//Inactive 7//Normal 8//Reject 9//Void
