/* For license and copyright information please see the LEGAL file in the code repository */

package inventory_p

type ReferenceType uint8

const (
	ReferenceType_Unset        ReferenceType = iota
	ReferenceType_Production                 // ProductionID
	ReferenceType_Invoice                    // InvoiceID
	ReferenceType_Order                      // ProductOrderID
	ReferenceType_Transfer                   // InventoryChangeID
	ReferenceType_ChangeOwner                // UserID
	ReferenceType_SplitProduct               // Split to small size product || Split from upper size product
	ReferenceType_Void                       //
	// ReferenceType_
)
