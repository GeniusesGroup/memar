/* For license and copyright information please see the LEGAL file in the code repository */

package invoice

// FinancialCredit ---Read locale description in lawStructure---
type Law struct {
	AppInstanceID      [32]byte // Store to remember which app instance set||chanaged this record!
	
	BuyerID [16]byte
	PayerID [16]byte // support just one user as payer??
	// Products []ProductList
}
